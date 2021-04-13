import json
import boto3
from boto3.dynamodb.conditions import Key
import decimal

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
            if (task["tags"])[0] == machine["machine_id"]:
                if task["date_created"] >= start_time and task["date_resolved"] <= end_time:
                    times.append((task["date_created"],task["date_resolved"]))
        avail[machine["machine_id"]] = times
    return avail


# calls getMachineById to get machine data
# input format: ?machine_id=<id>
def GetMachineStatusHandler(event, context):
    # Call function
    machines = list(GetMachines())
    tasks = list(GetTasks())

    body = json.loads(event["body"])
    start_time = body["start_time"]
    end_time = body["end_time"]

    availability = processAvailability(machines,tasks,start_time, end_time)


    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': json.dumps(availability,cls=DecimalEncoder)
    }


