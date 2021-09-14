import json
import boto3
from boto3.dynamodb.conditions import Key
import decimal
import time

dynamodb = boto3.resource('dynamodb')
dynamodb_client = boto3.client('dynamodb')

Visitors = dynamodb.Table('Visitors')
Visits = dynamodb.Table('Visits')


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return int(obj)
        elif isinstance(obj, set):
            return list(obj)
        return super(DecimalEncoder, self).default(obj)


def GetVisits(body):

    visits = Visits.scan()
    visits_list = visits["Items"]

    start_date = body["start_date"]
    end_date = body["end_date"]

    visits_in_tf = []

    for visit in visits_list:
        if int(visit["date_visited"]) >= start_date and int(
                visit["date_visited"]) <= end_date:
            visits_in_tf.append(visit)

    return visits_in_tf


# calls getMachineById to get machine data
# input format: ?machine_id=<id>
def GetVisitsHandler(event, context):
    # Call function
    body = event["body"]
    try:
        body["start_date"]
    except BaseException:
        body = {
            "start_date": 0,
            "end_date": int(time.time()) + 10
        }

    visitors = GetVisits(body)

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'

        },
        'body': json.dumps({
            'visits': visitors
        }, cls=DecimalEncoder)
    }
