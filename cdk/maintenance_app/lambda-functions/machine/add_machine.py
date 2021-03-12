import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
dynamodb_client = boto3.client('dynamodb')

#adds a new machine with its details to the Machines table
#also adds the machine id to the Machine_Types table
#machine type must already exist
def addMachine(id, machine_type, machine_name):
    
    #Table Resources
    machine_table = dynamodb.Table('Machines')
    machine_types = dynamodb.Table('Machine_Types')
   
    #Check if Machine already exists
    response = machine_table.query(
        KeyConditionExpression=Key('Machine_Id').eq(id)
    )

    #Return errror if it does
    if(len(response['Items']) > 0):
        return 0

    #Add new Machine to Machine Types
    machine_types.update_item(
        Key={
            'Machine_Type': machine_type,
        },
        UpdateExpression="ADD Machines :id",
        ExpressionAttributeValues={
            ':id': {id}
        },
    )

    #Define New Machine Object
    newMachine = {}
    newMachine['Machine_Id'] = id
    newMachine['Type'] = machine_type
    newMachine['Name'] = machine_name

    #Add New Machine to Db
    machine_table.put_item(Item=newMachine)
    
    #Success
    return 1

#input: ?machine_id=<id>&machine_type=<Type>&machine_name=<Name>
def addMachineHandler(event, context):

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
    #Check for Machine Id param
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
    #Check for Machine Type param
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
    #Check for Machine Name param
    if('machine_name' not in params):
        return{
            'statusCode': 400,
            'headers':{
                'Content-Type': 'text/plain'
            },
            'body': json.dumps({
                    'Message' : 'Failed to provide parameter: machine_name',
            }) 
        }

    #Set parameter values    
    machine_type = params['machine_type']
    id = params['machine_id']
    machine_type = params['machine_type']
    machine_name = params['machine_name']

    #Call Function
    flag = addMachine(id, machine_type, machine_name)

    #Error Message
    if(flag == 0):
        return {
            'statusCode': 400,
            'headers':{
                'Content-Type': 'text/plain'
            },
            'body': "Machine already exists"
        }
    #Success Message
    else:
        return {
            'statusCode': 200,
            'headers':{
                'Content-Type': 'text/plain'
            },
            'body': "Added machine: " + machine_type + " " + id + " " + machine_name
        }

