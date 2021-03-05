import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
dynamodb_client = boto3.client('dynamodb')

#get machine data given an id
def getMachineById(id):

    #Machine Table
    table = dynamodb.Table('Machines')
    
    #Get Machine By Id
    response = table.query(
        KeyConditionExpression=Key('Machine_Id').eq(id)
    )

    #Send Machine
    return response['Items'][0]

#calls getMachineById to get machine data
#input format: ?machine_id=<id>
def viewMachineHandler(event, context):
    
    params = event['queryStringParameters']
    
    #Check for query params
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
    #Check for Machine Id
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

    #Set Param Value
    id = params['machine_id']
    
    #Call function
    machine = getMachineById(id)

    #Convert Task Set to List
    if 'Tasks' in machine:
        machine['Tasks'] = list(machine['Tasks'])
    
    #Send Response
    return{
        'statusCode': 200,
        'headers':{
            'Content-Type': 'text/plain'
        },
        'body': json.dumps(machine)
    }