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
#Parent_Table = dynamodb.Table('Parent_Tasks')
#Child_Table = dynamodb.Table('Child_Tasks')
#Machine_Table = dynamodb.Table('Machines')

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


def CreateTask(json):

    new_task = Task()

    # Parameters
    new_task.task_id = json.task_id
    new_task.task_name = json.task_name
    new_task.decsription = json.description
    new_task.assigned_to = json.assigned_to
    new_task.creation_date = json.creation_date
    new_task.completion_date = json.completion_date
    new_task.tags = json.tags
    new_task.status = json.status




    # Generate unique parent id
    parentId = str(uuid.uuid4())


    # Put new task into the tasks database
    Tasks.put_item(
        Item = json.dumps(new_task)
    )

    return parentId


def CreateTaskHandler(event, context):
    reqHeaders = ['TaskName', 'Description', 'Frequency', 'MachineId',
                 'MachineName', 'CompletionTime', 'StartDate']

    # Get request body data
    data = json.loads(event.body)

    # Return client error if no string params
    if (data is None):
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': json.dumps({
                'Message': 'Failed to provide query string parameters.'
            })
        }

    # Check for each parameter we need
    for name in reqHeaders:
        if (name not in data):
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'text/plain'
                },
                'body': json.dumps({
                    'Message': 'Failed to provide parameter: ' + name
                })
            }

    try:
        # Call function
        result = CreateTask(data)

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