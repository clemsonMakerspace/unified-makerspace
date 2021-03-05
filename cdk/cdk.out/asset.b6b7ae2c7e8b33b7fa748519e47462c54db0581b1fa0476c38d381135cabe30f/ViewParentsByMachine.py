import json
import boto3
from boto3.dynamodb.conditions import Key

#Dynamo DB Resource
dynamodb = boto3.resource('dynamodb')

#Table Objects
Machine_Table = dynamodb.Table('Machines')
Parent_Table = dynamodb.Table('Parent_Tasks')

def ViewParentsByMachine(params):

    #Parameters
    machineId = params['MachineId']

    #List Vars
    parentIds = []
    parentTasks = []

    #Get Machine
    machine = Machine_Table.query(
        KeyConditionExpression=Key('Machine_Id').eq(machineId)
    )['Items'][0]

    #Get Parent Task Ids From Machine
    if 'Tasks' in machine:
        parentIds = list(machine['Tasks'])

    #Get Each Parent Task
    for pid in parentIds:
        
        #Query Parent Task
        pTask = Parent_Table.query(
            KeyConditionExpression=Key('Parent_Id').eq(pid)
        )['Items'][0]

        #Delete Decimal Attr
        del pTask['Active']

        #Add Task to List
        parentTasks.append(pTask)

    return parentTasks

def ViewParentsByMachineHandler(event, context):
    
    reqParams = ['MachineId']

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
        result = ViewParentsByMachine(paramVals)

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