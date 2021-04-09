# FROM MAKERSPACE MANAGER LAMBDA APPLICATION


import boto3
import json
import uuid
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from boto3.dynamodb.conditions import Key
from api.models import Task

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Get Table Objects

# DEPRECATED: TO REMOVE
# Parent_Table = dynamodb.Table('Parent_Tasks')
# Child_Table = dynamodb.Table('Child_Tasks')
# Machine_Table = dynamodb.Table('Machines')

Tasks = dynamodb.Table('Tasks')


# Function for Calculating Due Dates for Children
def CalculateNextDate(start, freq, add):
    # Convert start date to DateTime
    startDateTime = datetime.strptime(str(start), '%Y%m%d')

    # Add offset for each frequency category
    if freq == 'Daily':
        startDateTime += timedelta(days=add)
    elif freq == 'Weekly':
        startDateTime += timedelta(weeks=add)
    elif freq == 'Monthly':
        startDateTime += relativedelta(months=add)

    # Return NextDate as String
    return startDateTime.strftime('%Y%m%d')


def CreateTask(data):
    new_task = data["body"]

    new_task = Task(new_task["task_id"], new_task["task_name"], new_task["description"], new_task["assigned_to"],
                    new_task["date_created"], new_task["date_completed"], new_task["tags"], new_task["task_status"])


    # Put new task into the tasks eventbase
    Tasks.put_item(
        Item = new_task.__dict__
    )

    return 1


def CreateTaskHandler(event, context):
    reqHeaders = ['task_id', 'task_name', 'description', 'assigned_to', 'date_created', 'date_completed', 'tags',
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
        result = CreateTask(event)

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