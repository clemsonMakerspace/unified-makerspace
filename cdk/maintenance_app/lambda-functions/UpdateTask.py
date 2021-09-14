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
        Key={
            'task_id': task_id
        },
        UpdateExpression="set #st=:s",
        ExpressionAttributeValues={
            ':s': body['state'],
        },
        ExpressionAttributeNames={
            '#st': "status"
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
                'Content-Type': 'text/plain',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH'
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
                'Content-Type': 'text/plain',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH'
            },
            'body': json.dumps({'Message': "Task successfully updated."})
        }
    except Exception as e:
        # Return exception with response
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'text/plain',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PATCH'
            },
            'body': json.dumps({
                'Message': str(e)
            })
        }
