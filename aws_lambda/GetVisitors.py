import json
import boto3
from boto3.dynamodb.conditions import Key
import decimal

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


def GetVisitors(body):
    start_time = body["start_time"]
    end_time = body["end_time"]

    visits = Visits.scan()
    visits_list = visits["Items"]

    visits_in_tf = []


    for visit in visits_list:
        if int(visit["sign_in_time"]) >= start_time and int(visit["sign_out_time"]) <= end_time:
            visits_in_tf.append(visit)

    return visits_in_tf


# calls getMachineById to get machine data
# input format: ?machine_id=<id>
def GetVisitorsHandler(event, context):
    # Call function
    body = json.loads(event["body"])


    visitors = GetVisitors(body)

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': json.dumps(visitors,cls=DecimalEncoder)
    }


