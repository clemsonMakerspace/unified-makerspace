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

    def __init__(self, original_table, users_table):

        if users_table is None:
            # Default Behavior in Prod
            # Get the service resource.
            dynamodb = boto3.resource('dynamodb')
            # Get the table name.
            USERS_TABLE_NAME = os.environ["USERS_TABLE_NAME"]
            # Get table objects
            self.users = dynamodb.Table(USERS_TABLE_NAME)
        else:
            self.users = users_table

        if original_table is None:
            dynamodb = boto3.resource('dynamodb')
            ORIGINAL_TABLE_NAME = os.environ["ORIGINAL_TABLE_NAME"]
            self.original = dynamodb.Table(ORIGINAL_TABLE_NAME)
        else:
            self.original = original_table

    def add_user_info(self, user_info):
        # Get the current date at which the user registers.
        timestamp = datetime.datetime.now()

        original_response = self.original.put_item(
            Item={
                'PK': user_info['username'],
                'SK': str(timestamp),
                'firstName': user_info['firstName'],
                'lastName': user_info['lastName'],
                'Gender': user_info['Gender'],
                'DOB': user_info['DOB'],
                'Grad_date': user_info['Grad_Date'],
                'Major': user_info['Major'],
                'Minor': user_info.get('Minor', [])
            },
        )

        # Add the user to the original table
        new_table_response = self.users.put_item(
            Item={
                'username': user_info['username'],
                'register_time': str(timestamp),
                'firstName': user_info['firstName'],
                'lastName': user_info['lastName'],
                'Gender': user_info['Gender'],
                'DOB': user_info['DOB'],
                'Grad_date': user_info['Grad_Date'],
                'Major': user_info['Major'],
                'Minor': user_info.get('Minor', [])
            },
        )

        # TODO: Decide between the response to return.
        return original_response['ResponseMetadata']['HTTPStatusCode']

    def handle_register_user_request(self, request, context):
        HEADERS = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': os.environ["DOMAIN_NAME"],
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
        response = self.add_user_info(user_info)
        # Send response
        return {
            'headers': HEADERS,
            'statusCode': response
        }


register_user_function = RegisterUserFunction(None, None)


def handler(request, context):
    # Register user information from the makerspace/register console
    # Since this will be hit in prod, it will go ahead and hit our prod
    # dynamodb table
    return register_user_function.handle_register_user_request(
        request, context)
