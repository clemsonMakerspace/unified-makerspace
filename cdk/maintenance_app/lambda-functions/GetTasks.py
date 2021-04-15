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
def GetTasks():
    tasks = Tasks.scan()
    return tasks["Items"]


def GetTasksHandler(event, context):
    reqHeaders = ['task_id', 'task_name', 'description', 'assigned_to', 'date_created', 'date_resolved', 'tags',
                  'task_status']


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
        result = list(GetTasks())

        # Send Response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': json.dumps(result, cls=DecimalEncoder)
        }
    except Exception as e:
        # Return exception with response
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': json.dumps({
                'Message': str(e)
            })
        }