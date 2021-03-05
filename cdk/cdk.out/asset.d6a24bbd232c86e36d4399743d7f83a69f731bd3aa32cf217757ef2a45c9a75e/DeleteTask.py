import json
import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

#Get Table Objects
Parent_Table = dynamodb.Table('Parent_Tasks')
Child_Table = dynamodb.Table('Child_Tasks')
Machine_Table = dynamodb.Table('Machines')

#Needs to do the following:
    #Mark Parent As InActive
    #Mark Children As InActive
    #Remove Upcoming Children From DB
    #Remove Task From Machine
def DeleteTask(params):
    
    #Get Parameters
    parentId = params['ParentId']

    #Mark Parent Inactive
    Parent_Table.update_item(
        Key={
            'Parent_Id': parentId,
        },
        UpdateExpression="SET Active = :zero",
        ExpressionAttributeValues={
            ':zero': 0
        },
    )

    #Query Children Using GSI
    children = Child_Table.query(
        TableName= 'Child_Tasks', 
        IndexName= "Parent_Index",
        KeyConditionExpression=
            Key('Parent_Id').eq(parentId)
    )['Items']

    #Todays DueDate Key
    today = datetime.now().strftime('%Y%m%d')

    #Mark Children Inactive
    for child in children:

        #Mark Inactive if passed due
        if child['Due_Date'] < today:
            Child_Table.update_item(
                TableName= 'Child_Tasks', 
                Key={
                    'Parent_Id': parentId,
                    'Due_Date' : child['Due_Date']
                },
                UpdateExpression="SET Active = :zero",
                ExpressionAttributeValues={
                    ':zero': 0
                },
            )
        #Delete if upcoming
        else:
            Child_Table.delete_item(
                Key = {
                    'Parent_Id' : parentId,
                    'Due_Date' : child['Due_Date']
                }
            )

    #Get Machine ID of Task
    machineId = Parent_Table.query(
        KeyConditionExpression=
            Key('Parent_Id').eq(parentId)
    )['Items'][0]['Machine_Id']

    #Remove Task from Machine
    Machine_Table.update_item(
        Key={
            'Machine_Id': machineId,
        },
        UpdateExpression = "DELETE Tasks :oldTask",
        ExpressionAttributeValues={
            ':oldTask': {parentId}
        },
    )
        
    return "Successfully deleted task."

def DeleteTaskHandler(event, context):
    
    reqParams = ['ParentId']

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
        result = DeleteTask(paramVals)

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