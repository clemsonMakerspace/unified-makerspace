# FROM MAKERSPACE MANAGER LAMBDA APPLICATION
import boto3
import json
import uuid
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from boto3.dynamodb.conditions import Key
from api.models import Visitor


# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Get Table Objects
Visitors = dynamodb.Table("Visitors")



def CreateVisitor(data):
    new_visitor = json.loads(data["body"])

    new_visitor = Visitor(new_visitor["visitor_id"],new_visitor["first_name"],new_visitor["last_name"],
                          new_visitor["major"],new_visitor["degree_type"])

    # Put new task into the tasks eventbase
    Visitors.put_item(
        Item=new_visitor.__dict__
    )

    return 1


def CreateVisitorHandler(event, context):

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
        result = CreateVisitor(event)

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