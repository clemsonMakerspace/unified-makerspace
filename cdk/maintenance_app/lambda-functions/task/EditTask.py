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

    #Return NextDate as Int
    return startDateTime.strftime('%Y%m%d')

def updateName(pid, name):

    #Update Name of Task in Parent Table
    Parent_Table.update_item(
        Key={
            'Parent_Id': pid,
        },
        UpdateExpression="SET #task_name = :newName",
        ExpressionAttributeValues={
            ':newName': name
        },
        ExpressionAttributeNames= {
            "#task_name": "Name"
        }
    )

    #Grab all Children from Parent
    children = Child_Table.query(
        TableName= 'Child_Tasks', 
        IndexName= "Parent_Index",
        KeyConditionExpression=
            Key('Parent_Id').eq(pid)
    )['Items']

    #Update Each Child's Name
    for child in children:
        Child_Table.update_item(
            TableName= 'Child_Tasks', 
            Key={
                'Parent_Id': pid,
                'Due_Date': child['Due_Date']
            },
            UpdateExpression="SET Task_Name = :newName",
            ExpressionAttributeValues={
                ':newName': name
            },
        )

def updateMachine(pid, newMid, oldMid):

    #Update Machine_Id in Parent Table
    Parent_Table.update_item(
        Key={
            'Parent_Id': pid,
        },
        UpdateExpression="SET Machine_Id = :newMid",
        ExpressionAttributeValues={
            ':newMid': newMid
        },
    )

    #Remove Task from Old Machine
    Machine_Table.update_item(
        Key={
            'Machine_Id': oldMid,
        },
        UpdateExpression = "DELETE Tasks :oldTask",
        ExpressionAttributeValues={
            ':oldTask': {pid}
        },
    )

    #Add Task to New Machine
    Machine_Table.update_item(
        Key={
            'Machine_Id': newMid,
        },
        UpdateExpression="ADD Tasks :newTask",
        ExpressionAttributeValues={
            ':newTask': {pid}
        },
    )

    #Grab all Children of Parent
    children = Child_Table.query(
        TableName= 'Child_Tasks', 
        IndexName= "Parent_Index",
        KeyConditionExpression=
            Key('Parent_Id').eq(pid)
    )['Items']

    #Grab Machine Name of New Machine
    machineName = Machine_Table.query(
        KeyConditionExpression=
            Key('Machine_Id').eq(newMid)
    )['Items'][0]['Name']

    #Update Each Child's Machine_Name
    for child in children:
        Child_Table.update_item(
            Key={
                'Parent_Id': pid,
                'Due_Date': child['Due_Date']
            },
            UpdateExpression="SET Machine_Name = :newName",
            ExpressionAttributeValues={
                ':newName': machineName
            },
        )

def updateDescription(pid, desc):

    #Only Update Parent Table for Description
    Parent_Table.update_item(
        Key={
            'Parent_Id': pid,
        },
        UpdateExpression="SET Description = :newDesc",
        ExpressionAttributeValues={
            ':newDesc': desc
        },
    )

def updateTime(pid, time):

    #Update Time in Parent Table
    Parent_Table.update_item(
        Key={
            'Parent_Id': pid,
        },
        UpdateExpression="SET Completion_Time = :newTime",
        ExpressionAttributeValues={
            ':newTime': time
        },
    )

    #Calculate todays date
    today = datetime.now().strftime("%Y%m%d")

    #Grab all (Future) Children for Parent
    children = Child_Table.query(
        TableName= 'Child_Tasks', 
        IndexName= "Parent_Index",
        KeyConditionExpression=
            Key('Parent_Id').eq(pid) &
            Key('Due_Date').gt(today)
    )['Items']

    #Update Each Child's Time
    for child in children:
        Child_Table.update_item(
            Key={
                'Parent_Id': pid,
                'Due_Date': child['Due_Date']
            },
            UpdateExpression="SET Due_Time = :newTime",
            ExpressionAttributeValues={
                ':newTime': time
            },
        )

def updateFrequency(pid, freq, start):

    #Update Frequency in Parent Table
    Parent_Table.update_item(
        Key={
            'Parent_Id': pid,
        },
        UpdateExpression="SET Frequency = :newFreq",
        ExpressionAttributeValues={
            ':newFreq': freq
        },
    )

    #Calculate todays date
    today = datetime.now().strftime("%Y%m%d")

    #Grab future children of Parent - maybe filter by complete
    children = Child_Table.query(
        TableName= 'Child_Tasks', 
        IndexName= "Parent_Index",
        KeyConditionExpression=
            Key('Parent_Id').eq(pid) &
            Key('Due_Date').gte(today),
        FilterExpression="Completed = :comp",
        ExpressionAttributeValues= {
            ':comp' : 0
        }
    )['Items']

    #Delete Future Children
    for child in children:
        Child_Table.delete_item(
            Key = {
                'Parent_Id' : pid,
                'Due_Date' : child['Due_Date']
            }
        )

    #Create Child Instances from new Start Date
    for i in range (0, 10):

        #Calculate Due Date for each child instance
        nextDue = CalculateNextDate(start, freq, i)

        #Add Child Instance to DB
        Child_Table.put_item(
            Item = {
                'Parent_Id' : pid,
                'Due_Date': nextDue,
                'Due_Time': children[0]['Due_Time'],
                'Machine_Name': children[0]['Machine_Name'],
                'Task_Name' : children[0]['Task_Name'],
                'Frequency': freq,
                'Completed' : 0,
                'Late'  : 0,
                'Completed_By' : '',
                'Completed_DateTime': '',
                'Active' : 1
            }
        )

def EditTask(params): 

    #Required Parameters
    parentId = params['ParentId']
    taskName = params['TaskName']
    machineId = params['MachineId']
    description = params['Description']
    completionTime = params['CompletionTime']
    frequency = params['Frequency']

    #Query Parent Task to check for changes
    parent = Parent_Table.query(
        KeyConditionExpression=
            Key('Parent_Id').eq(parentId)
    )['Items'][0]
    
    msg = ""

    #Update Frequency
    if parent['Frequency'] != frequency:
        
        #Check for StartDate before completing request
        if 'StartDate' not in params:
            return "Failed to provide parameter: StartDate - Required when Updating Frequency" 
        
        updateFrequency(parentId, frequency, params['StartDate'])
        msg += "    - Frequency\n"

    #Update Name
    if parent['Name'] != taskName:
        updateName(parentId, taskName)
        msg += "    - Task Name\n"

    #Update Machine
    if parent['Machine_Id'] != machineId:
        oldMachineId = parent['Machine_Id']
        updateMachine(parentId, machineId, oldMachineId)
        msg += "    - Machine\n"

    #Update Description
    if parent['Description'] != description:
        updateDescription(parentId, description)
        msg += "    - Description\n"

    #Update Completion Time
    if parent['Completion_Time'] != completionTime:
        updateTime(parentId, completionTime)
        msg += "    - Completion Time\n"


    if msg == "":
        return "No updates made to task."
    else:
        return "Update the following: \n" + msg

def EditTaskHandler(event, context):

    reqParams = ['ParentId', 'TaskName', 'Description', 
                'Frequency', 'MachineId', 'CompletionTime']

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
        result = EditTask(paramVals)

        #Send User Error for Specific Scenarios
        if ("Failed" in result):
            return {
                'statusCode': 400,
                'headers':{
                    'Content-Type': 'text/plain'
                },
                'body': json.dumps(result)
            }
        #Send Response if Successful
        else:
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