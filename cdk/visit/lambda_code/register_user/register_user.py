import json
import boto3
from boto3.dynamodb.conditions import Key
import os
import datetime


class RegisterUserFunction():
    """
    This class wraps the function of the lambda so we can more easily test
    it with moto. In production, we will continue to pass the stood-up
    dynamodb table to the handler itself. However, when initializing this class,
    we can choose to instead initialize it with a mocked version of the
    dynamodb table.
    """

    def __init__(self, table):

        if table is None:
            # Default Behavior in Prod
            # Get the service resource.
            dynamodb = boto3.resource('dynamodb')
            # Get the table name.
            TABLE_NAME = os.environ["TABLE_NAME"]
            # Get table objects
            self.users = dynamodb.Table(TABLE_NAME)
        else:
            self.users = table

    def addUserInfo(self, user_info):
        # Get the current date at which the user registers.
        timestamp = datetime.datetime.now()

        response = self.users.put_item(
            Item={
                'PK': user_info['username'],
                'SK': str(timestamp),
                'firstName': user_info['firstName'],
                'lastName': user_info['lastName'],
                'Gender': user_info['Gender'],
                'DOB': user_info['DOB'],
                'Grad_date': user_info['Grad_Date'],
                'Major': user_info['Major'],
                'Minor': user_info['Minor']
            },
        )

        return response['ResponseMetadata']['HTTPStatusCode']

    def handle_register_user_request(self, request, context):
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
                'body': json.dumps({
                    "Message": "Failed to provide parameters"
                })
            }

        # Get all of the user information from the json file
        user_info = json.loads(request["body"])
        # Call Function
        response = self.addUserInfo(user_info)
        # Send response
        return {
            'headers': HEADERS,
            'statusCode': response
        }


def handler(request, context):
    # Register user information from the makerspace/register console
    # Since this will be hit in prod, it will go ahead and hit our prod dynamodb table
    return RegisterUserFunction(None).handle_register_user_request(request, context)
