import boto3
import uuid
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from boto3.dynamodb.conditions import Key, Attr

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

#Get Table Objects
Parent_Table = dynamodb.Table('Parent_Tasks')
Child_Table = dynamodb.Table('Child_Tasks')


#Function for Calculating Due Dates for Children
def CalculateNextDate(start, freq, add):

    #Convert start to DateTime
    nextDate = datetime.strptime(str(start), '%Y%m%d')

    #Add offset for each frequency category
    if freq == 'Daily':
        nextDate += timedelta(days=add)
    elif freq == 'Weekly':
        nextDate += timedelta(weeks=add)
    elif freq == 'Monthly' :
        nextDate += relativedelta(months=add)

    #Return NextDate as String
    return nextDate.strftime('%Y%m%d')


#Function that will add child following last child
def AddChildTask(last, freq):

    #Get Date for newly created task
    nextDue = CalculateNextDate(last['Due_Date'], freq, 1)

    #Craft New Task
    newTask = {
        'Parent_Id' : last['Parent_Id'],
        'Due_Date': nextDue,
        'Due_Time': last['Due_Time'],
        'Machine_Name': last['Machine_Name'],
        'Task_Name' : last['Task_Name'],
        'Frequency': last['Frequency'],
        'Completed' : 0,
        'Late'  : 0,
        'Completed_By' : '',
        'Completed_DateTime': '',
        'Active' : 1
    }

    #Add Child Instance to DB
    Child_Table.put_item(
        Item = newTask
    )

    return newTask

def MarkLateTasks():

    #Today's Key
    today = datetime.now().strftime('%Y%m%d')

    #Get Today's Incomplete Child Tasks
    children = Child_Table.query(
        KeyConditionExpression=Key('Due_Date').eq(today),
        FilterExpression=Attr('Completed').eq(0)
    )['Items']

    #Mark Each Task Late
    for child in children:
        Child_Table.update_item(
            Key={
                'Parent_Id': child['Parent_Id'],
                'Due_Date': today
            },
            UpdateExpression="SET Late = :one",
            ExpressionAttributeValues={
                ':one': 1
            },
        )

def MaintainTasksHandler(event, context):

    #First Mark Today's Incomplete Task Late
    MarkLateTasks()

    #Get All Active Parent Tasks
    parents = Parent_Table.scan(
        FilterExpression=Attr('Active').eq(1)
    )['Items']

    #Check Each Parent Tasks Children
    for pTask in parents:

        #Calculate todays date
        today = datetime.now().strftime("%Y%m%d")

        #Grab future children of Parent
        children = Child_Table.query(
            TableName= 'Child_Tasks', 
            IndexName= "Parent_Index",
            KeyConditionExpression=
                Key('Parent_Id').eq(pTask['Parent_Id']) &
                Key('Due_Date').gt(today)
        )['Items']


        #If Less than 10 child tasks remaining
        while len(children) < 10:

            #Sort children by due date
            sortedChildren = sorted(children, key=lambda c: c['Due_Date']) 

            #Add another child after last child
            newChild = AddChildTask(children[-1], pTask['Frequency'])

            #Append to children list
            children.append(newChild)
