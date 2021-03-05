import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
dynamodb_client = boto3.client('dynamodb')

#edit name of machine given id of machine
def editMachineName(id, newName):
    
    #Table Resource
    table = dynamodb.Table('Machines')

    #Check that Machine Exists
    response = table.query(
        KeyConditionExpression=Key('Machine_Id').eq(id)
    )
    
    #Send error if does not exist
    if(len(response['Items']) == 0):
        return 0

    #Update Machine Name
    table.update_item(
        Key={
            'Machine_Id': id,
        },
        UpdateExpression="SET #N = :newname",
        ExpressionAttributeValues={
            ":newname": newName
        },
        ExpressionAttributeNames={
            "#N": "Name"
        }
    )

    #Send Success
    return 1

#input: ?machine_id=<id>&new_name=<name>
def editMachineNameHandler(event, context):
    
    params = event['queryStringParameters']
    
    #Check for query string params
    if(params is None):
        return{
            'statusCode': 400,
            'headers':{
                'Content-Type': 'text/plain'
            },
            'body': json.dumps({
                'Message' : 'Failed to provide query string parameters.'
            })
        }
    
    #Check for Machine id
    if('machine_id' not in params):
        return{
            'statusCode': 400,
            'headers':{
                'Content-Type': 'text/plain'
            },
            'body': json.dumps({
                    'Message' : 'Failed to provide parameter: machine_id',
            }) 
        }
    
    #Check for new name
    if('new_name' not in params):
        return{
            'statusCode': 400,
            'headers':{
                'Content-Type': 'text/plain'
            },
            'body': json.dumps({
                    'Message' : 'Failed to provide parameter: new_name',
            }) 
        }

    #Set param values
    id = params['machine_id']
    newName = params['new_name']

    #Call function
    flag = editMachineName(id, newName)
    
    #Send error response
    if(flag == 0):
        return {
            'statusCode': 400,
            'headers':{
                'Content-Type': 'text/plain'
            },
            'body': "Machine does not exist"
        }
    #Success response
    else:
        return {
            'statusCode': 200,
            'headers':{
                'Content-Type': 'text/plain'
            },
            'body': "Edited machine: " + id + " with new name of " + newName
        }

