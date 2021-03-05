import boto3
import json
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr

#Get the service resource.
dynamodb = boto3.resource('dynamodb')

#Table Objects
Machine_Table = dynamodb.Table('Machines')
Parent_Table = dynamodb.Table('Parent_Tasks')
Child_Table = dynamodb.Table('Child_Tasks')

#Needs to do the following
    #Get Parent Tasks From Machine
    #Grab upcoming task in child db (use DueDate/MachineId)
    #Make Sure to Filter Inactive Tasks and Completed Tasks
def ViewUpcomingMachineTasks(params):

    #Parameters
    daysForward = int(params['DaysForward'])
    machineId = params['MachineId']

    #Get Machine
    machine = Machine_Table.query(
        KeyConditionExpression=Key('Machine_Id').eq(machineId)
    )['Items'][0]

    
    parents = []
    tasks = []
    
    #Get Parent Tasks from Machine
    if 'Tasks' in machine:
        parents = list(machine['Tasks'])

    #Query Parent Tasks
    for pid in parents:

        #DueDate Ranges
        today = datetime.now().strftime("%Y%m%d")
        future = (datetime.now() + timedelta(days=daysForward)).strftime("%Y%m%d")

        #Grab upcoming children of Parent between range
        children = Child_Table.query(
            TableName= 'Child_Tasks', 
            IndexName= "Parent_Index",
            KeyConditionExpression=
                Key('Parent_Id').eq(pid) &
                Key('Due_Date').between(today, future),
            FilterExpression=Attr('Active').eq(1)&Attr('Completed').eq(0)
        )['Items']

        #Remove Decimal Fields
        for child in children:
            del child['Active']
            del child['Completed']
            del child['Late']

        #Append Task to List
        tasks = tasks + children

    return tasks

def ViewMachineUpcomingTasksHandler(event, context):
    
    reqParams = ['DaysForward', 'MachineId']

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
        result = ViewUpcomingMachineTasks(paramVals)

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