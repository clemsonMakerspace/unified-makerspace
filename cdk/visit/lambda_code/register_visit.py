import json
import datetime
import boto3
from boto3.dynamodb.conditions import Key
import os

 # Get the service resource.
dynamodb = boto3.resource('dynamodb')
# Get the table name. 
table_name = os.environ["TABLE_NAME"]
# Get table objects
visits = dynamodb.Table(table_name)

def addVisitEntry(data): 
    current_user = json.loads(data["body"])["username"]
    # Get the current date at which the user logs in. 
    temp_date = datetime.datetime.now()

    # Current date formatting MM/DD/YYYY.  
    visit_date = str((temp_date.month)) + "/" + str((temp_date.day)) + "/" + str((temp_date.year))

    # Create the dynamodb item to put in the table. 
    new_visit = {
        "PK" : visit_date, 
        "SK" : current_user
    }
    # Add the item to the table. 
    visits.put_item(Item = new_visit)

    # Confirm this item is in the table by running a query on it. 
    response = visits.query(
        KeyConditionExpression=Key('PK').eq(visit_date)
    )

    in_place = 1
    for user in response['Items']:
        if(user['PK'] == current_user):
            in_place = 0

    if in_place == 0:
        return "Unverified"
    else:
        return "Verified"

def handler(request, context):
    """
    Register the input of a user (namely, the username) from the makerspace console.

    This should:

    1. Check whether this user has visited before by looking for a
       sentinel record in the table
    2. Trigger a registration workflow if this is the first time for that user
    3. Place a visit entry into the table
    """
    res = addVisitEntry(request)
    
    # return client error if no string params
    if (request is None):
        return {
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'statusCode': 400,
            'body':json.dumps({
                "Message": "Failed to provide parameters"
            })
        }

    return {
        'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
        'statusCode': 200,
        'body':json.dumps({
            "Message": "Success",
            "Verification": res
        })
    }
