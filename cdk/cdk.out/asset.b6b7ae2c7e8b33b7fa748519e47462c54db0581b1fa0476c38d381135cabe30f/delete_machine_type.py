import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
dynamodb_client = boto3.client('dynamodb')

def deleteMachineType(machine_type):
    
    #Table Resources
    table = dynamodb.Table('Machine_Types')

    #Delete Machine Type
    response = table.delete_item(
        Key={
            'Machine_Type': machine_type
        }
    )

    #Send Response
    return response

#input: ?machine_type=<Type>
def deleteMachineTypeHandler(event, context):
    
    params = event['queryStringParameters']
    
    #Check for query strin params
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
    
    #Set param value
    machine_type = params['machine_type']
    
    #Call Function
    deleteMachineType(machine_type)
    
    #Return response
    return{
        'statusCode': 200,
        'headers':{
            'Content-Type': 'text/plain'
        },
        'body': "Deleted machine type: " + machine_type
    }