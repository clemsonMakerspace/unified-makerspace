# FROM MAKERSPACE MANAGER LAMBDA APPLICATION


import boto3
import json
import uuid
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from boto3.dynamodb.conditions import Key
#from api.models import Task

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Get Table Objects

# DEPRECATED: TO REMOVE
# Parent_Table = dynamodb.Table('Parent_Tasks')
# Child_Table = dynamodb.Table('Child_Tasks')
# Machine_Table = dynamodb.Table('Machines')

Tasks = dynamodb.Table('Tasks')


def ResolveTask(data):

    body = json.loads(data["body"])
    task_id = body["task_id"]

    response = Tasks.update_item(
        Key = {
            'task_id': task_id
        },
        UpdateExpression="set task_status=:s",
        ExpressionAttributeValues={
            ':s': 'Completed'
        },
        ReturnValues="UPDATED_NEW"
    )
    return response


def ResolveTaskHandler(event, context):
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
        result = ResolveTask(event)

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