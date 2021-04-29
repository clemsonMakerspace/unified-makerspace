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


def UpdateTask(data):

    body = json.loads(data["body"])
    task_id = body["task_id"]

    response = Tasks.update_item(
        Key = {
            'task_id': task_id
        },
        UpdateExpression="set task_name=:n, description=:d, date_created=:c, date_resolved=:o, tags=:t, "
                         "assigned_to=:a, status=:s",
        ExpressionAttributeValues={
            ':n': body["task_name"],
            ':d': body["description"],
            ':c': body["date_created"],
            ':o': body["date_resolved"],
            ':t': body["tags"],
            ':a': body['assigned_to'],
            ':s': body['status'],
        },
        ReturnValues="UPDATED_NEW"
    )
    return response


def UpdateTaskHandler(event, context):

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
        result = UpdateTask(event)

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
                'Content-Type': 'text/plain'
            },
            'body': json.dumps({
                'Message': str(e)
            })
        }