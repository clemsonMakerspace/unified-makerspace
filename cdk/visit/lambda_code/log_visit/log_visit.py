import json
import datetime
import dateutil.tz
from pydoc import cli
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import logging
import traceback
import sys
import os
import re


class LogVisitFunction():
    """
    This function will be used to wrap the functionality of the lambda
    so we can more easily test with pytest.
    """

    def __init__(self, original_table, visits_table, users_table, ses_client):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        if original_table is None:
            dynamodb = boto3.resource('dynamodb')
            ORIGINAL_TABLE_NAME = os.environ['ORIGINAL_TABLE_NAME']
            self.original = dynamodb.Table(ORIGINAL_TABLE_NAME)
        else:
            self.original = original_table

        if visits_table is None:
            # Get the service resource.
            dynamodb = boto3.resource('dynamodb')
            # Get the table name.
            VISITS_TABLE_NAME = os.environ["VISITS_TABLE_NAME"]
            # Get table objects
            self.visits = dynamodb.Table(VISITS_TABLE_NAME)
        else:
            self.visits = visits_table

        if users_table is None:
            # Get the service resource.
            dynamodb = boto3.resource('dynamodb')
            # Get the table name.
            USERS_TABLE_NAME = os.environ["USERS_TABLE_NAME"]
            # Get table objects
            self.users = dynamodb.Table(USERS_TABLE_NAME)
        else:
            self.users = users_table

        if ses_client is None:
            AWS_REGION = os.environ['AWS_REGION']
            self.client = boto3.client('ses', region_name=AWS_REGION)
        else:
            self.client = ses_client

    def isUserRegistered(self, current_user):
        """
        true if the user has registered
        """
        original_table_response = self.original.query(
            KeyConditionExpression=Key('PK').eq(current_user)
        )
        return original_table_response['Count'] != 0

    # This code was written following the example from:
    # https://docs.aws.amazon.com/ses/latest/DeveloperGuide/send-using-sdk-python.html
    def registrationWorkflow(self, current_user):
        # This address must be verified with Amazon SES.
        SENDER = "no-reply@visit.cumaker.space"

        email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
        if not email_regex.match(current_user):
            current_user = current_user + "@clemson.edu"

        RECIPIENT = current_user

        # One could consider using a configuration set here.
        # To learn more about them please visit:
        # https://docs.aws.amazon.com/ses/latest/DeveloperGuide/using-configuration-sets.html

        SUBJECT = "Clemson University Makerspace Registration"
        BODY_TEXT = ("Hello " + current_user + ",\n"
                     "Our records indicate that you have not registered as an existing user.\n"
                     "Please go to visit.cumaker.space/register to register as an existing user.\n"
                     )
        # The character encoding for the email.
        CHARSET = "UTF-8"
        # Create a new SES resource and specify a region.

        # Try to send the email.
        try:
            response = self.client.send_email(
                Destination={
                    'ToAddresses': [
                        RECIPIENT,
                    ],
                },
                Message={
                    'Body': {
                        'Text': {
                            'Charset': CHARSET,
                            'Data': BODY_TEXT,
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': SUBJECT,
                    },
                },
                ReplyToAddresses=["makerspace@clemson.edu"],
                Source=SENDER,
                # If we were using a configuration set we would need the following line.
                # ConfigurationSetName=CONFIGURATION_SET,
            )

        # Display an error if something goes wrong.
        except ClientError as e:
            self.logger.error(e.response['Error']['Message'])

    def addVisitEntry(self, current_user, location, tool):
        
        # Get the current date at which the user logs in.
        eastern_tz = dateutil.tz.gettz('US/Eastern')
        visit_date = datetime.datetime.now(tz=eastern_tz)

        # Add the item to the tables.
        visit_response = self.visits.put_item(
            # PK = Partition Key = Visit Date
            # SK = Sort Key = Username or Email Address

            Item={
                'visit_time': int(visit_date.timestamp()),
                'username': current_user,
                'location': location,
                'tool': tool,
            },
        )

        original_response = self.original.put_item(
            Item={
                'PK': visit_date.strftime('%Y-%m-%d %H:%M:%S'),
                'SK': current_user,
                'tool': tool or ' ',
                'location': location or ' ',
            },
        )

        return original_response['ResponseMetadata']['HTTPStatusCode']

    def handle_log_visit_request(self, request, context):
        """
        Log the input of a user (namely, the username) from the makerspace console.
        This should:
        1. Check whether this user has visited before by looking for a
        sentinel record in the table
        2. Trigger a registration workflow if this is the first time for that user
        3. Place a visit entry into the table
        """

        HEADERS = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': os.environ["DOMAIN_NAME"],
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        }

        def bad_request(body):
            return {
                'headers': HEADERS,
                'statusCode': 400,
                'body': json.dumps(body)
            }

        # if no request is provided (should never be the case because of gateway evocation)
        if (request is None):
            return bad_request({'Message': 'No request provided'})
        
        # get the body of the request
        body = json.loads(request.get('body', "{}"))

        # get the users username
        try:
            username = body['username']
        except KeyError:
            return bad_request({'Message': 'Missing parameter: username'})

        # get the users location
        location = None 
        try:
            location = body['location']
        except KeyError:
            self.logger.warn('location parameter was not provided')
        
        # get what tool the user is using
        tool = None
        try:
            tool = body['tool']
        except KeyError:
            self.logger.warn('tool parameter was not provided')

        # send user the registration link if not registered
        user_registered = self.isUserRegistered(username)
        if not user_registered:
            self.registrationWorkflow(username)

        # add the visit entry
        status_code = self.addVisitEntry(username, location, tool)

        # Send response
        return {
            'headers': HEADERS,
            'statusCode': status_code,
            'body': json.dumps({
                "was_user_registered": user_registered,                
            })
        }


log_visit_function = LogVisitFunction(None, None, None, None)

def handler(request, context):
    # This will be hit in prod, and will connect to the stood-up dynamodb
    # and Simple Email Service clients.
    return log_visit_function.handle_log_visit_request(request, context)
