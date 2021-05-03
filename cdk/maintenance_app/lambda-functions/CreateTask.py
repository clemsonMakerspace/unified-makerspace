# FROM MAKERSPACE MANAGER LAMBDA APPLICATION


import boto3
import time
import json
import uuid
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from boto3.dynamodb.conditions import Key
from api.models import Task
from CreateMachine import *

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Get Table Objects

# DEPRECATED: TO REMOVE
# Parent_Table = dynamodb.Table('Parent_Tasks')
# Child_Table = dynamodb.Table('Child_Tasks')
# Machine_Table = dynamodb.Table('Machines')

Tasks = dynamodb.Table('Tasks')
Machines = dynamodb.Table('Machines')



def CreateTask(data):
    new_task = json.loads(data["body"])
    
    machine_name = (new_task["tags"])[0]

    new_task = Task(str(uuid.uuid4().hex[:6]), new_task["task_name"], new_task["description"], new_task["person"],
                    int(time.time()), 0, new_task["tags"], 0)

    
    machines = Machines.scan()
    machines_list = machines["Items"]
    
    
    if machine_name not in machines_list and machine_name != "*":
        CreateMachine(machine_name,0)
    
    # Put new task into the tasks eventbase
    Tasks.put_item(
        Item = new_task.__dict__
    )

    return 1


def CreateTaskHandler(event, context):

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
        result = CreateTask(event)

        # Send Response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/plain',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
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