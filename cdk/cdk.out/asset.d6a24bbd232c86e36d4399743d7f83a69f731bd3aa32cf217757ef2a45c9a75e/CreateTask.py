import boto3
import json
import uuid
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from boto3.dynamodb.conditions import Key

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

#Get Table Objects
Parent_Table = dynamodb.Table('Parent_Tasks')
Child_Table = dynamodb.Table('Child_Tasks')
Machine_Table = dynamodb.Table('Machines')

#Function for Calculating Due Dates for Children
def CalculateNextDate(start, freq, add):

    #Convert start date to DateTime
    startDateTime = datetime.strptime(str(start), '%Y%m%d')

    #Add offset for each frequency category
    if freq == 'Daily':
        startDateTime += timedelta(days=add)
    elif freq == 'Weekly':
        startDateTime += timedelta(weeks=add)
    elif freq == 'Monthly' :
        startDateTime += relativedelta(months=add)

    #Return NextDate as String
    return startDateTime.strftime('%Y%m%d')

def CreateTask(params):

    #Parameters
    taskName = params['TaskName']
    description = params['Description']
    frequency = params['Frequency']
    machineId = params['MachineId']
    machineName = params['MachineName']
    time = params['CompletionTime']
    startDate = params['StartDate']

    #Generate unique parent id
    parentId = str(uuid.uuid4())
    
    #Create Parent Task Object
    Parent_Table.put_item(
        Item = {
            'Parent_Id' : parentId,
            'Machine_Id' : machineId, 
            'Name' : taskName,
            'Description': description,
            'Frequency': frequency,
            'Active' : 1,
            'Start_Date' : startDate,
            'Completion_Time' : time,
        }
    )

    #Add Parent Task to Machine Tasks List
    Machine_Table.update_item(
        Key={
            'Machine_Id': machineId,
        },
        UpdateExpression="ADD Tasks :newTask",
        ExpressionAttributeValues={
            ':newTask': {parentId}
        },
    )

    #Create Child Instances from Start Date
    for i in range (0, 10):

        #Calculate Due Date for each child instance
        nextDue = CalculateNextDate(startDate, frequency, i)

        #Add Child Instance to DB
        Child_Table.put_item(
            Item = {
                'Parent_Id' : parentId,
                'Due_Date': nextDue,
                'Due_Time': time,
                'Machine_Name': machineName,
                'Frequency': frequency,
                'Task_Name' : taskName,
                'Completed' : 0,
                'Late'  : 0,
                'Completed_By' : '',
                'Completed_DateTime': '',
                'Active' : 1
            }
        )

    return parentId

def CreateTaskHandler(event, context):

    reqParams = ['TaskName', 'Description', 'Frequency', 'MachineId', 
                'MachineName', 'CompletionTime', 'StartDate']

    #Get Query Params
    paramVals = event["queryStringParameters"]

    #Return client error if no string params
    if (paramVals is None):
        return{
            'statusCode': 400,
            'headers':{
                'Content-Type': 'text/plain'
            },
            'body': json.dumps({
                'Message' : 'Failed to provide query string parameters.'
            })
        }

    #Check for each parameter we need
    for name in reqParams:
        if (name not in paramVals):
            return {
                'statusCode': 400,
                'headers':{
                    'Content-Type': 'text/plain'
                },
                'body': json.dumps({
                    'Message' : 'Failed to provide parameter: ' + name
                }) 
            }       

    try:
        #Call function
        result = CreateTask(paramVals)

        #Send Response
        return {
            'statusCode': 200,
            'headers':{
                'Content-Type': 'text/plain'
            },
            'body': json.dumps(result)
        }
    except Exception as e:
        #Return exception with response
        return {
            'statusCode': 500,
            'headers':{
                'Content-Type': 'text/plain'
            },
            'body': json.dumps({
                'Message' : str(e)
            })
        }