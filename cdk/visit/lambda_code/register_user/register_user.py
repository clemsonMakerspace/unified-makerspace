import json
import pdb
import dateutil.tz
import boto3
from boto3.dynamodb.conditions import Key
import os
import datetime
import time
from typing import Tuple


def process_grad_date(grad_date: str) -> Tuple[str, int]:
    """
    Infers the graduation semester and year from grad_date
    grad_date: str
        The graduation date in the format 'YYYY-MM-DD'
    Returns:
        A tuple of the semester and year.
    """
    year = grad_date[:4]
    month = grad_date[5:7]
    print(month)
    if month in ['04', '05', '06']:
        semester = 'Spring'
    elif month in ['07', '08', '09']:
        semester = 'Summer'
    elif month in ['11', '12', '01']:
        semester = 'Fall'
    else:
        raise ValueError(
            'Month passed was not April, May, June, July, August, September, November, December or January')

    return semester, year


class RegisterUserFunction():
    """
    This class wraps the function of the lambda so we can more easily test
    it with moto. In production, we will continue to pass the stood-up
    dynamodb table to the handler itself. However, when initializing this class,
    we can choose to instead initialize it with a mocked version of the
    dynamodb table.
    """

    def __init__(self, original_table, users_table, dynamodbclient):
        if dynamodbclient is None:
            self.dynamodbclient = boto3.client('dynamodb')
        else:
            self.dynamodbclient = dynamodbclient

        self.USERS_TABLE_NAME = os.environ["USERS_TABLE_NAME"]
        if users_table is None:
            dynamodbresource = boto3.resource('dynamodb')
            self.users = dynamodbresource.Table(self.USERS_TABLE_NAME)
        else:
            self.users = users_table

        self.ORIGINAL_TABLE_NAME = os.environ["ORIGINAL_TABLE_NAME"]
        if original_table is None:
            self.original = dynamodbresource.Table(
                self.ORIGINAL_TABLE_NAME)
        else:
            self.original = original_table

    def add_user_info(self, user_info):

        # register the user in the old combined table
        original_response = self.original.put_item(
            Item={
                'PK': user_info['username'],
                'SK': str(datetime.datetime.now()),
                'firstName': user_info['firstName'],
                'lastName': user_info['lastName'],
                'Gender': user_info['Gender'],
                'DOB': user_info['DOB'],
                'Position': user_info['UserPosition'],
                'GradSemester': user_info.get('GradSemester', ' '),
                'GradYear': user_info.get('GradYear', ' '),
                'Major': ', '.join(sorted(user_info.get('Major', []))),
                'Minor': ', '.join(sorted(user_info.get('Minor', []))),
                'last_updated':user_info.get('last_updated','')
            },
        )

        # format Grad_Date if the frontend does not provide the new format
        if 'Grad_Date' in user_info:
            # Add the user to the original table
            grad_sem, grad_year = process_grad_date(user_info['Grad_Date'])
        else:
            grad_sem = user_info.get('GradSemester', ' ')
            grad_year = user_info.get('GradYear', ' ')

        # type marshall all majors/minors to be strings
        # https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_AttributeValue.html
        majors = [{"S": s} for s in user_info.get('Major', [])]
        minors = [{"S": s} for s in user_info.get('Minor', [])]
        
        

        timestamp = int(time.time())

        # dict for entry into the users table
        user_table_item = {
            'username': {'S': user_info['username']},
            'register_time': {'N': str(timestamp)},
            'first_name': {'S': user_info['firstName']},
            'last_name': {'S': user_info['lastName']},
            'gender': {'S': user_info['Gender']},
            'date_of_birth': {'S': user_info['DOB']},
            'position': {'S': user_info['UserPosition']},
            'grad_semester': {'S': grad_sem},
            'grad_year': {'S': grad_year},
            'majors': {'L': majors},
            'minors': {'L': minors},
        }

        # if the json is from a test request it will have this ttl attribute
        if "last_updated" in user_info:
            user_table_item['last_updated'] = {"N":str(user_info['last_updated'])}

        user_table_response = self.dynamodbclient.put_item(
            TableName=self.USERS_TABLE_NAME,
            Item=user_table_item
            )



        if original_response['ResponseMetadata']['HTTPStatusCode'] != user_table_response['ResponseMetadata']['HTTPStatusCode']:
            raise Exception("One of Original Table or User Table update failed.")

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


register_user_function = RegisterUserFunction(None, None, None)


def handler(request, context):
    # Register user information from the makerspace/register console
    # Since this will be hit in prod, it will go ahead and hit our prod
    # dynamodb table
    return register_user_function.handle_register_user_request(
        request, context)
