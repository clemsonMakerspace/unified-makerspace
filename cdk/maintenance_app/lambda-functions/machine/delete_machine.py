import json
import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
dynamodb_client = boto3.client('dynamodb')

#deletes machine and marks assiciated tasks as inactive
def deleteMachine(id, machine_type):
    
    #Table Resources
    machine_table = dynamodb.Table('Machines')
    parent_table = dynamodb.Table('Parent_Tasks')
    child_table = dynamodb.Table('Child_Tasks')
    type_table = dynamodb.Table('Machine_Types')

    #Get machine
    machine = machine_table.query(
        KeyConditionExpression=Key('Machine_Id').eq(id)
    )['Items'][0]

    parents = []

    #Get Parent Tasks from Machine
    if 'Tasks' in machine:
        parents = list(machine['Tasks'])

    #Each task for machine
    for pid in parents:
                
        #mark parent tasks as inactive
        parent_table.update_item(
            Key={
                'Parent_Id': pid
            },
            UpdateExpression="SET Active = :inactive",
            ExpressionAttributeValues={
                ':inactive': 0
            },
        )

        #Today Due Date
        today = datetime.now().strftime('%Y%m%d')
        
        #Grab children of task
        children = child_table.query(
            TableName= 'Child_Tasks', 
            IndexName= "Parent_Index",
            KeyConditionExpression=
                Key('Parent_Id').eq(pid)
        )['Items']

        #Each child task of parent
        for child in children:      
            
            #Mark Inactive if passed due
            if child['Due_Date'] < today:
                child_table.update_item(
                    TableName= 'Child_Tasks', 
                    Key={
                        'Parent_Id': pid,
                        'Due_Date' : child['Due_Date']
                    },
                    UpdateExpression="SET Active = :zero",
                    ExpressionAttributeValues={
                        ':zero': 0
                    },
                )
            #Delete if upcoming
            else:
                child_table.delete_item(
                    Key = {
                        'Parent_Id' : pid,
                        'Due_Date' : child['Due_Date']
                    }
                )
    

    #delete machine from machine table
    response = machine_table.delete_item(
        Key={
            'Machine_Id': id
        }
    )

    #delete machine from machine types table
    try:    
        type_table.update_item(
            Key={
                'Machine_Type': machine_type
            },
            UpdateExpression="DELETE Machines :id",
            ExpressionAttributeValues={
                ':id': {id}
            },
        )
    except:
        print("Machine could not be delete from Machine Type.")
        
    return response

#input: ?machine_id=<id>&machine_type=<Type
def deleteMachineHandler(event, context):
    
    params = event['queryStringParameters']
    
    #Check for Query string params
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

    #Set parameter values
    id = params['machine_id']
    machine_type = params['machine_type']

    #Call function
    deleteMachine(id, machine_type)
    
    #Send Response
    return{
        'statusCode': 200,
        'headers':{
            'Content-Type': 'text/plain'
        },
        'body': "Deleted machine: " + id
    }