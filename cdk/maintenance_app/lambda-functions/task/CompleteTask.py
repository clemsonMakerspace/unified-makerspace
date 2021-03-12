import json
import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

#Get Table Objects
Child_Table = dynamodb.Table('Child_Tasks')

#Mark Child Instance As Complete
def CompleteTask(params):

    #Parameters
    dueDate = params['DueDate']
    parentId = params['ParentId']
    completedBy = params['CompletedBy']

    #Mark Task as Completed
    Child_Table.update_item(
        Key={
            'Parent_Id': parentId,
            'Due_Date': dueDate
        },
        UpdateExpression =
            "SET Completed = :one, Completed_By = :who, Completed_DateTime = :when",
        ExpressionAttributeValues={
            ':one': 1,
            ':who': completedBy,
            ':when' : str(datetime.now().timestamp()), 
        }
    )

    return "Task Completed"

def CompleteTaskHandler(event, context):

    reqParams = ['DueDate', 'ParentId', 'CompletedBy']

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
        result = CompleteTask(paramVals)

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