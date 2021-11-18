import json
import boto3
from boto3.dynamodb.conditions import Key
import os

# Get the service resource.
dynamodb = boto3.resource('dynamodb')
# Get the table name. 
TABLE_NAME = os.environ["TABLE_NAME"]
# Get table objects
users = dynamodb.Table(TABLE_NAME)

def addUserInfo(user_info): 
    response = visits.put_item(
        Item = {
            #'PK' : user_info['username'],
            #'SK' : user_info['firstName'],
            #'lastName' : user_info['lastName'],
            #'Gender' : user_info['Gender'],
            #'DOB' : user_info['DOB'],
            #'Grad_date' : user_info['Grad_date']
            #'Major' : user_info['Major']
            #'Minor' : user_info['Minor']
        },
    )

    return response['ResponseMetadata']['HTTPStatusCode']

def handler(request, context):
    # Register user information from the makerspace/register console
    
    HEADERS = {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': 'https://visit.cumaker.space/register',
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

        # Get all of the user information from the json file
        user_info = json.loads(request["body"])
        # Call Function
        response = addUserInfo(user_info)
        # Send response
        return { 
            'headers' : HEADERS,
            'statusCode' : response,
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