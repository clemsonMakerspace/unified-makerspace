import json
import datetime
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

    def checkRegistration(self, current_user):
        print("Checking registration for: " + current_user)
        original_table_response = self.original.query(
            KeyConditionExpression=Key('PK').eq(current_user)
        )

        return original_table_response['Count']

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

    def addVisitEntry(self, current_user, location):
        # Get the current date at which the user logs in.
        visit_date = datetime.datetime.now().timestamp()
        # Convert visit_date to human-readable format
        visit_date = datetime.datetime.fromtimestamp(
            visit_date).strftime('%Y-%m-%d %H:%M:%S')

        # Add the item to the tables.
        visit_response = self.visits.put_item(
            # PK = Partition Key = Visit Date
            # SK = Sort Key = Username or Email Address

            Item={
                'visit_time': str(visit_date),
                'username': current_user,
                'location': location,
            },
        )

        original_response = self.original.put_item(
            Item={
                'PK': str(visit_date),
                'SK': current_user,
                'location': location,
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
        # return client error if no string params

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

        try:
            # Get the username from the request body.
            username = json.loads(request["body"])["username"]
            location = ' '
            try:
                location = json.loads(request["body"])["location"]
            except Exception as e:
                exception_type, exception_value, exception_traceback = sys.exc_info()
                traceback_string = traceback.format_exception(
                    exception_type, exception_value, exception_traceback)
                err_msg = json.dumps({
                    "errorType": "MissingParameter",
                    "errorMessage": "Missing parameter: location",
                    "errorTrace": traceback_string
                })
                self.logger.warn(err_msg)

            # Check if this user has registered before.
            registration = self.checkRegistration(username)

            # If the user is not in the system, send a registration link.
            if registration == 0:
                self.registrationWorkflow(username)
                # One could consider setting res = some other number here in order to
                # bring up a page That lets the user know in order to sign in they
                # have to check their email and register with the Makerspace.

                # Call Function
            res = self.addVisitEntry(username, location)

            # Send response
            return {
                'headers': HEADERS,
                'statusCode': res
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


log_visit_function = LogVisitFunction(None, None, None, None)


def handler(request, context):
    # This will be hit in prod, and will connect to the stood-up dynamodb
    # and Simple Email Service clients.
    return log_visit_function.handle_log_visit_request(request, context)
