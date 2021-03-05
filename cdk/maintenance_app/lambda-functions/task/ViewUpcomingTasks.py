import boto3
import json
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr

#Get the service resource.
dynamodb = boto3.resource('dynamodb')

#Table Object
Child_Table = dynamodb.Table('Child_Tasks')

#Needs to do the following
    #Grab upcoming task in child db (use DueDate)
    #Make Sure to Filter Inactive Tasks and Completed Tasks
def ViewUpcomingTasks(params):

    #Parameters
    daysForward = int(params['DaysForward'])
    
    tasks = []

    #Iterate from today to 'N' days forward
    for addDay in range(0, daysForward + 1):

        #Calculate key for due date
        dueDate = (datetime.now()+timedelta(days=addDay)).strftime('%Y%m%d')
        
        #Get incomplete tasks due
        children = Child_Table.query(
            KeyConditionExpression=Key('Due_Date').eq(dueDate),
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

def ViewUpcomingTasksHandler(event, context):
    
    reqParams = ['DaysForward']

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
        result = ViewUpcomingTasks(paramVals)

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