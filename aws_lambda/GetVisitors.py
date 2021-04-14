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

    visitors = Visitors.scan()
    visitors_list = visitors["Items"]

    visits = Visits.scan()
    visits_list = visits["Items"]

    visits_in_tf = []

    for visitor in visitors_list:
        for visit in visits_list:
            if visit["visitor_id"] == visitor["visitor_id"]:
                if visit["sign_in_time"] >= start_time and visit["sign_out_time"] <= end_time:
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


