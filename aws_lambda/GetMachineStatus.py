import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
dynamodb_client = boto3.client('dynamodb')


# get machine data given an id
def getMachineById(id):
    # Machine Table
    table = dynamodb.Table('Machines')

    # Get Machine By Id
    response = table.query(
        KeyConditionExpression=Key('Machine_Id').eq(id)
    )

    # Send Machine
    return response['Items'][0]


# calls getMachineById to get machine data
# input format: ?machine_id=<id>
def getMachineStatusHandler(event, context):
    params = event['queryStringParameters']

    # Check for query params
    if (params is None):
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': json.dumps({
                'Message': 'Failed to provide query string parameters.'
            })
        }
    # Check for Machine Id
    if ('machine_id' not in params):
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': json.dumps({
                'Message': 'Failed to provide parameter: machine_id',
            })
        }

    # Check for time/date
    if ('date' not in params):
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': json.dumps({
                'Message': 'Failed to provide parameter: date',
            })
        }

    if ('time' not in params):
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': json.dumps({
                'Message': 'Failed to provide parameter: time',
            })
        }


    # Set Param Value
    id = params['machine_id']

    date = params['date']
    time = params['time']



    # Call function
    machine = getMachineById(id)

    # Convert Task Set to List
    if 'Tasks' in machine:
        machine['Tasks'] = list(machine['Tasks'])
        for task in machine['Tasks']:
            if task['Start_Date'] == date:
                return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'text/plain'
                    },
                    'body': json.dumps({'Status': 'Unavailable'})
                }
        else:
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'text/plain'
                },
                'body': json.dumps({'Status': 'Free'})
            }
    # no tasks associated with machine, so it must be free
    else:
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': json.dumps({'Status': 'Free'})
        }


