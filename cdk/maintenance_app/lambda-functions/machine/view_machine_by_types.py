import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
dynamodb_client = boto3.client('dynamodb')

#gets machine id by type in Machine_Types
def getMachineIdsByType(type):
    
    #Machine Types Table
    table = dynamodb.Table('Machine_Types')
    
    #Get Machine Type
    response = table.query(
        KeyConditionExpression=Key('Machine_Type').eq(type)
    )

    #Send Ids From Machine Type
    if 'Machines' in response['Items'][0]:
        return list(response['Items'][0]['Machines'])
    
    #Return Empty List if No Machine
    else:
        return []
        

#Gets Machine Details By Id
def getMachineById(id):
    
    #Machine Table Resource
    table = dynamodb.Table('Machines')
    
    #Get Machines
    response = table.query(
        KeyConditionExpression=Key('Machine_Id').eq(id)
    )

    #Send Machine
    return response['Items'][0]

#calls getMachineIdByType first to get the machine id and then calls
#getMachineById to get the machine information
#currently it returns list of ids instead of all information
#input: ?machine_type=<Type> (case sensitive)
def viewMachineByTypesHandler(event, context):
    
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
    
    #Check for machine_type
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

    #Set param values
    machine_type = params['machine_type']

    #Get Machine Ids of Type
    machine_ids = getMachineIdsByType(machine_type)

    ret_obj = []
    
    #Each id in machine ids list
    for mid in machine_ids:
        
        #Get Machine By Id
        machine = getMachineById(mid)

        #Convert Task Set to List
        if 'Tasks' in machine:
            machine['Tasks'] = list(machine['Tasks'])
        
        #Add Machine to List
        ret_obj.append(machine)

    #Send Response
    return{
        'statusCode': 200,
        'headers':{
            'Content-Type': 'text/plain'
        },
        'body': json.dumps(ret_obj)
    }
