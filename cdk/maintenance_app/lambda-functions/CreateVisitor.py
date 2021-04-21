# FROM MAKERSPACE MANAGER LAMBDA APPLICATION
import boto3
import json
import uuid
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from boto3.dynamodb.conditions import Key
from api.models import Visitor, Visit

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Get Table Objects
Visitors = dynamodb.Table("Visitors")
Visits = dynamodb.Table("Visits")


def CreateVisitor(data):
    json_data = json.loads(data["body"])
    hardware_id = json_data["hardware_id"]
    new_visitor = json_data["visitor"]

    new_visitor_obj = Visitor(hardware_id, new_visitor["degree_type"], new_visitor["first_name"],
                              new_visitor["last_name"], new_visitor["major"], str(uuid.uuid4().hex[:10]))

    visits = Visits.scan()
    visits_list = visits["Items"]

    new_visit = Visit

    for visit in visits_list:

        if visit["visitor_id"] == new_visitor_obj.visitor_id:
            new_visit = Visit(str(uuid.uuid4().hex[:10]), new_visitor_obj.visitor_id, "0", int(time.time()), 0)
            break
    else:
        new_visit = Visit(str(uuid.uuid4().hex[:10]), new_visitor_obj.visitor_id, "1", int(time.time()), 0)

    Visits.put_item(
        Item=new_visit.__dict__
    )

    # Put new task into the tasks eventbase
    Visitors.put_item(
        Item=new_visitor_obj.__dict__
    )

    return "Created new visitor: " + new_visitor_obj.visitor_id + " " + new_visitor_obj.first_name + " " + new_visitor_obj.last_name


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
                'Content-Type': 'text/plain',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'

            },
            'body': json.dumps({
                'Message': str(e)
            })
        }