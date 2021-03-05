import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
dynamodb_client = boto3.client('dynamodb')

#Adds a new machine type with an empty array
def addMachineType(machine_type):
    
    #Table Resource
    table = dynamodb.Table('Machine_Types')

    #Check for existing Machine Types
    response = table.query(
        KeyConditionExpression=Key('Machine_Type').eq(machine_type)
    )

    #Return error if already in db
    if(len(response['Items']) > 0):
        return 0
    
    #Add New Machine Type
    table.put_item(
        Item = {
            'Machine_Type' : machine_type,
        }
    )

    #Success
    return 1
    
#input: ?machine_type=<New Type>
def addMachineTypeHandler(event, context):
    
    params = event['queryStringParameters']
    
    #Check for parameters
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
    
    #Check for Machine Type
    if('machine_type' not in params):
        return{
            'statusCode': 400,
            'headers':{
                'Content-Type': 'text/plain'
            },
            'body': json.dumps({
                    'Message' : 'Failed to provide parameter: machine_type',
            }) 
        }
    
    #Pass Parameter
    machine_type = params['machine_type']
    
    #Call functions
    flag = addMachineType(machine_type)
    
    #Check for failure
    if(flag == 0):
        return {
            'statusCode': 400,
            'headers':{
                'Content-Type': 'text/plain'
            },
            'body': "Machine type already exists"
        }
    #Success message
    else:
        return {
            'statusCode': 200,
            'headers':{
                'Content-Type': 'text/plain'
            },
            'body': "Added machine type: " + machine_type
        }