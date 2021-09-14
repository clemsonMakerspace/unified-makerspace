# FROM MAKERSPACE MANAGER LAMBDA APPLICATION


import boto3
import json
from boto3.dynamodb.conditions import Key


# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Get Table Objects
Machines = dynamodb.Table('Machines')


def DeleteMachine(body):

    machine_name = body["machine_name"]

    Machines.delete_item(
        Key={
            'machine_name': machine_name
        }
    )

    return 1


def DeleteMachineHandler(event, context):

    # Return client error if no string params
    if (event is None):
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': json.dumps({
                'Message': 'Failed to provide query string parameters.'
            })
        }

    try:
        # Call function
        result = DeleteMachine(json.loads(event["body"]))

        # Send Response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': json.dumps(result)
        }
    except Exception as e:
        # Return exception with response
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'text/plain',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'

            },
            'body': json.dumps({
                'Message': str(e)
            })
        }
