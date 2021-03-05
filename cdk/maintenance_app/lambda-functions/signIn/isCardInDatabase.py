import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
dynamodb_client = boto3.client('dynamodb')


# adds a new machine with its details to the Machines table
# also adds the machine id to the Machine_Types table
# machine type must already exist
def isCardInDatabase(id):
    # Table Resources
    table = dynamodb.Table('MakerspaceUser')


    # Check if user already exists
    response = table.query(
        KeyConditionExpression=Key('PK').eq(id)
    )

    # Return errror if it does
    if (len(response['Items']) > 0):
        return True
    else:
        return False



# input:
def isCardInDatabaseHandler(event, context):
    params = event['queryStringParameters']

    reqParams = ["PK"]

    # Check for query params
    if (params is None):
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': json.dumps({
                'Message': 'Failed to provide query string parameters.'
            })
        }

    for param in reqParams:
        if (param not in params):
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'text/plain'
                },
                'body': json.dumps({
                    'Message': 'Failed to provide parameter: ' + param
                })
            }


    # Set parameter values
    id = params["id"]


    # Call Function
    flag = isCardInDatabase(id)

    # Error Message
    if (flag == True):
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': "User already exists in system."
        }
    # Success Message
    else:
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': "User not already in system."
        }

