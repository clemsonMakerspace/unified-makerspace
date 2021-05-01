import json
import boto3
from boto3.dynamodb.conditions import Key
import decimal
import time

dynamodb = boto3.resource('dynamodb')
dynamodb_client = boto3.client('dynamodb')

Machines = dynamodb.Table('Machines')
Tasks = dynamodb.Table('Tasks')


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return int(obj)
        elif isinstance(obj, set):
            return list(obj)
        return super(DecimalEncoder, self).default(obj)


# get machine data given an id
def GetMachines():
    machines = Machines.scan()
    return machines["Items"]


def GetTasks():
    tasks = Tasks.scan()
    return tasks["Items"]


def processAvailability(machines, tasks, start_time, end_time):
    avail = {}
    for machine in machines:
        times = []
        for task in tasks:
            if (task["tags"])[0] == machine["machine_name"]:

                if int(task["date_created"]) >= int(start_time) and int(task["date_created"]) <= int(end_time):
                    print("true2")
                    if int(task["date_resolved"]) == 0:
                        times.append((int(task["date_created"]), int(time.time())))
                    else:
                        times.append((int(task["date_created"]), int(task["date_resolved"])))
        times.sort()
        avail[machine["machine_name"]] = times
    return avail


# calls getMachineById to get machine data
# input format: ?machine_id=<id>
def GetMachinesStatusHandler(event, context):
    # Call function
    machines = list(GetMachines())
    tasks = list(GetTasks())

    body = json.loads(event["body"])

    start_time = int(body["start_date"]) / 1000
    end_time = int(body["end_date"]) / 1000
    print(start_time)
    print(end_time)

    availability = processAvailability(machines, tasks, start_time, end_time)

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps({'machines': availability}, cls=DecimalEncoder)
    }


