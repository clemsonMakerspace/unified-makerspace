import json
import datetime
import boto3
from boto3.dynamodb.conditions import Key
import os

# Get the service resource.
dynamodb = boto3.resource('dynamodb')
# Get the table name. 
TABLE_NAME = os.environ["TABLE_NAME"]
# Get table objects
visits = dynamodb.Table(TABLE_NAME)

def addVisitEntry(current_user): 
    
    # Get the current date at which the user logs in. 
    visit_date = datetime.datetime.now().timestamp()

    # Add the item to the table. 
    response = visits.put_item(
        Item = {
            'PK' : str(visit_date),
            'SK' : current_user
        },
    )

    return response['ResponseMetadata']['HTTPStatusCode']


def handler(request, context):
    """
    Register the input of a user (namely, the username) from the makerspace console.

    This should:

    1. Check whether this user has visited before by looking for a
       sentinel record in the table
    2. Trigger a registration workflow if this is the first time for that user
    3. Place a visit entry into the table
    """
    
    # return client error if no string params

    HEADERS = {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': 'https://visit.cumaker.space',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            }
    

    if (request is None):
        return {
            'headers': HEADERS,
            'statusCode': 400,
            'body':json.dumps({
                "Message": "Failed to provide parameters"
            })
        }
    
    try: 
        # Get the username from the request body.
        username = json.loads(request["body"])["username"]
        # Call Function
        res = addVisitEntry(username)

        # Send response
        return {
            'headers': HEADERS,
            'statusCode': res,
        }

    except Exception as e:
        # Return exception with response
        return {
            'headers': HEADERS,
            'statusCode': 500,
            'body': json.dumps({
                'Message': str(e)
            })
        }