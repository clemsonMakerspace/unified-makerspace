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
        # Call Function
        res = addVisitEntry(request)

        # Send response
        return {
            'headers': HEADERS,
            'statusCode': 200,
            'body':json.dumps(res)
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
