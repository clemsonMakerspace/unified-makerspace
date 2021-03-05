import boto3
import json
from datetime import datetime
from boto3.dynamodb.conditions import Key

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

#Get Table Objects
Parent_Table = dynamodb.Table('Parent_Tasks')
Child_Table = dynamodb.Table('Child_Tasks')

def ViewTask(params):

    #Parameters
    dueDate = params['DueDate']
    parentId = params['ParentId']

    #Get the task using provided parameters
    task = Child_Table.query(
        KeyConditionExpression=
            Key('Due_Date').eq(dueDate) &
            Key('Parent_Id').eq(parentId)
    )['Items'][0]

    #Get the parent task as well
    parent = Parent_Table.query(
        KeyConditionExpression=
            Key('Parent_Id').eq(parentId)
    )['Items'][0]

    #Format Completion DateTime
    dueStr = dueDate + task['Due_Time']
    dueObj = datetime.strptime(dueStr, '%Y%m%d%H%M')

    #Build the object
    taskObject = {
        'Task' : task['Task_Name'],
        'Machine_Name' : task['Machine_Name'],
        'Frequency' : task['Frequency'],
        'Description' : parent['Description'],
        'Due' : dueObj.strftime("%c"),
        'Due_Date' :  dueDate,
        'Parent_Id' : parentId,
        'Start_Date' : parent['Start_Date']
    }

    return taskObject

def ViewTaskHandler(event, context):

    reqParams = ['DueDate', 'ParentId']

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
        result = ViewTask(paramVals)

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