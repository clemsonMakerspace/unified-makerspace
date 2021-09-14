# FROM MAKERSPACE MANAGER LAMBDA APPLICATION


import boto3
import json
import uuid
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from boto3.dynamodb.conditions import Key
from api.models import Machine

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Get Table Objects

# DEPRECATED: TO REMOVE
# Parent_Table = dynamodb.Table('Parent_Machines')
# Child_Table = dynamodb.Table('Child_Machines')
# Machine_Table = dynamodb.Table('Machines')

Machines = dynamodb.Table('Machines')


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


def CreateMachine(machine_name, machine_status):
    new_machine = Machine(machine_name, machine_status)

    # Put new task into the Machines eventbase
    Machines.put_item(
        Item=new_machine.__dict__
    )

    return 1


def CreateMachineBody(data):
    new_machine = json.loads(data["body"])

    new_machine = Machine(
        new_machine["machine_name"], new_machine["machine_status"])

    # Put new task into the Machines eventbase
    Machines.put_item(
        Item=new_machine.__dict__
    )

    return 1


def CreateMachineHandler(event, context):

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
        result = CreateMachineBody(event)

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
