import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
dynamodb_client = boto3.client('dynamodb')

#queries entire table
def viewMachineTypes():

    #Machine Types Table
    typeTable = dynamodb.Table('Machine_Types')
    machineTable = dynamodb.Table('Machines')
    
    #Scan Table
    response = typeTable.scan()
    
    #Results of Scan
    types = response['Items']

    #Extension of Scan
    while 'LastEvaluatedKey' in response:
        response = typeTable.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    #Each Machine Type
    for item in types:
        
        machineNames = []

        #Convert Machine Id Sets to List
        if 'Machines' in item:
            item['Machines'] = list(item['Machines'] )

        #Each Machine Id
        for mid in item['Machines']:
            
            #Get Machine
            machine = machineTable.query(
                KeyConditionExpression=Key('Machine_Id').eq(mid)
            )['Items'][0]

            #Add Name to List
            machineNames.append(machine['Name'])

        #Add List of Machine Names to Object
        item['Machine_Names'] = machineNames

    #Send Data
    return types

def viewMachineTypesHandler(event, context):
    
    #Call Function
    data = viewMachineTypes()

    #Send Response
    return{
        'statusCode': 200,
        'headers':{
            'Content-Type': 'text/plain'
        },
        'body': json.dumps(data)
    }

    

