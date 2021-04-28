# FROM MAKERSPACE MANAGER LAMBDA APPLICATION


import boto3
import json
from boto3.dynamodb.conditions import Key
import decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return int(obj)
        elif isinstance(obj, set):
            return list(obj)
        return super(DecimalEncoder, self).default(obj)


# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Get Table Objects
Tasks = dynamodb.Table('Tasks')


# Function for Calculating Due Dates for Children
def GetTasks(data):
    tasks = Tasks.scan()
    return tasks["Items"]


def GetTasksHandler(event, context):
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
        result = list(GetTasks(event))
        print(json.dumps(result, cls=DecimalEncoder))

        # Send Response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/plain',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'

            },
            'body': json.dumps({
                'tasks': result
            }, cls=DecimalEncoder)
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