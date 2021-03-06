import boto3
import json
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key, Attr

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

#Get Table Objects
Child_Table = dynamodb.Table('Child_Tasks')
Machine_Table = dynamodb.Table('Machines')

def ViewMachineHistory(params):

    #Parameters
    machineId = params['MachineId']
    daysBack = int(params['DaysBack'])

    #Denote variables
    items = []
    missed = 0
    complete = 0

    #Query Machine for Tasks
    machine = Machine_Table.query(
        KeyConditionExpression=Key('Machine_Id').eq(machineId)
    )['Items'][0]

    #Convert Set of Tasks to List
    if 'Tasks' in machine:
        machine['Tasks'] = list(machine['Tasks'])

    #Each Parent Tasks for Machine
    for pid in machine['Tasks']:

        #Calculate days
        yest = (datetime.now()-timedelta(days=1)).strftime('%Y%m%d')
        past = (datetime.now()-timedelta(days=daysBack)).strftime('%Y%m%d')

        #Query Child Table
        children = Child_Table.query(
            IndexName= "Parent_Index",
            KeyConditionExpression=
                Key('Parent_Id').eq(pid) &
                Key('Due_Date').between(past, yest),
            FilterExpression=Attr('Active').eq(1)
        )['Items']

        #Iterate through children
        for child in children:

            #Calculate Date Completed
            if child['Completed']:
                completed_on = datetime.fromtimestamp(
                    float(child['Completed_DateTime'])
                ).strftime('%c')
            else:
                completed_on = ''
                
            #Determine Task Status
            if child['Completed'] and child['Late']:
                status = 'Late'
            elif child['Completed']:
                status = 'Complete'
                complete += 1
            else:
                status = 'Missed'
                missed += 1

            #Add additional fields
            child['Completed_On'] = completed_on
            child['Status'] = status

            #Remove Fields
            del child['Active']
            del child['Late']
            del child['Completed']
            del child['Completed_DateTime']

            #Add task to list
            items.append(child)

    #Build result object
    result = {
        'Items': items,
        'Missed': missed,
        'Complete': complete
    }

    return result

def ViewMachineHistoryHandler(event, context):

    reqParams = ['DaysBack', 'MachineId']

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
        result = ViewMachineHistory(paramVals)

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