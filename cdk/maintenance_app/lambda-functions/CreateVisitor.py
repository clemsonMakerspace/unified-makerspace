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
    new_visitor = json.loads(data["body"])

    new_visitor = Visitor(new_visitor["visitor_id"],new_visitor["first_name"],new_visitor["last_name"],
                          new_visitor["major"],new_visitor["degree"])


    visits = Visits.scan()
    visits_list = visits["Items"]

    new_visit = Visit

    for visit in visits_list:

        if visit["visitor_id"] == new_visitor.visitor_id:
            new_visit = Visit(str(uuid.uuid4()),new_visitor.visitor_id,int(time.time()),"0")
            break
    else:
        new_visit = Visit(str(uuid.uuid4()),new_visitor.visitor_id,int(time.time()),"1")

    Visits.put_item(
        Item = new_visit.__dict__
    )

    # Put new task into the tasks eventbase
    Visitors.put_item(
        Item=new_visitor.__dict__
    )



    return 'Visitor ' + new_visitor.visitor_id + ' has been successfully created.'


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