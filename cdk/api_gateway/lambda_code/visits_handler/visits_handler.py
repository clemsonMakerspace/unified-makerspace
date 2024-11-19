import json
from pydoc import cli
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import logging
import os
import re
from datetime import datetime
from ..api_defaults import *

class LogVisitFunction():
    """
    This function will be used to wrap the functionality of the lambda
    so we can more easily test with pytest.
    """

    def __init__(self, visits_table, users_table, ses_client):
        # TODO: Setup CloudWatch Logs
        # Sets up CloudWatch logs and sets level to INFO
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        if visits_table is None:
            # Get the service resource.
            dynamodb = boto3.resource('dynamodb')
            # Get the table name.
            VISITS_TABLE_NAME = os.environ["VISITS_TABLE_NAME"]
            # Get table objects
            self.visits_table = dynamodb.Table(VISITS_TABLE_NAME)
        else:
            self.visits_table = visits_table

        if users_table is None:
            # Get the service resource.
            dynamodb = boto3.resource('dynamodb')
            # Get the table name.
            USERS_TABLE_NAME = os.environ["USERS_TABLE_NAME"]
            # Get table objects
            self.users_table = dynamodb.Table(USERS_TABLE_NAME)
        else:
            self.users_table = users_table

        if ses_client is None:
            AWS_REGION = os.environ['AWS_REGION']
            self.client = boto3.client('ses', region_name=AWS_REGION)
        else:
            self.client = ses_client
            
    # Main handler function
    def visits_handler(self, event, context):
        try:
            method_requires_body: list = ["POST", "PATCH"]

            response = buildResponse(statusCode = 400, body = {})
            http_method: str = event.get("httpMethod")
            resource_path: str = event.get("resource")

            # Get a user_id if needed
            user_id: str = ""
            if user_endpoint in resource_path:
                user_id = event['pathParameters'].get('user_id')

                # Make sure no '@' is in user_id
                if len(user_id.split("@")) > 1:
                    errorMsg: str = "user_id can't be an email."
                    body = { 'errorMsg': errorMsg }
                    return buildResponse(statusCode = 400, body = body)

            # Get the body data if needed
            data:dict = {}
            if http_method in method_requires_body:
                if 'body' not in event:
                    errorMsg: str = "REST method {http_method} requires a request body."
                    body = { 'errorMsg': errorMsg }
                    return buildResponse(statusCode = 400, body = body)
                data = json.loads(event['body'])

            # Try to get any query parameters
            try:
                query_parameters: dict = event['queryStringParameters']

                # Remove unknown query parameters
                for key in query_parameters:
                    if key not in VALID_QUERY_PARAMETERS:
                        del query_parameters[key]
                    if key in INT_QUERY_PARAMETERS:
                        query_parameters[key] = int(query_parameters[key])
            except:
                query_parameters: dict = {}

            # Visit information request handling
            if http_method == "GET" and resource_path == visits_path:
                response = self.get_all_visit_information(query_parameters)
            elif http_method == "POST" and resource_path == visits_path:
                response = self.create_user_visit_information(data)
            elif http_method == "GET" and resource_path == visits_param_path:
                response = self.get_user_visit_information(user_id, query_parameters)
                
            return response
        except:
            errorMsg: str = f"We're sorry, but something happened. Try again later."
            body = { 'errorMsg': errorMsg }
            return buildResponse(statusCode = 500, body = body)

    def isUserRegistered(self, current_user):
        """
        true if the user has registered
        """
        user_table_response = self.users_table.query(
            KeyConditionExpression=Key('user_id').eq(current_user)
        )
        return user_table_response['Count'] != 0

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
            
    #######################################
    # Visit information function handlers #
    #######################################
    def get_all_visit_information(self, query_parameters: dict):
        """
        Returns all visit information entries from the visit information table.

        :params query_parameters: A dictionary of parameter names and values to filter by.
        """

        if query_parameters:
            try:
                timestamp_expression = buildTimestampKeyExpression(query_parameters, 'timestamp')

            except InvalidQueryParameters as iqp:
                body = { 'errorMsg': str(iqp) }
                return buildResponse(statusCode = 400, body = body)

            try:
                key_expression = Key('_ignore').eq("1") & timestamp_expression
                items = queryByKeyExpression(self.visits_table, key_expression, GSI = TIMESTAMP_INDEX)

            except Exception as e:
                body = { 'errorMsg': "Something went wrong on the server." }
                return buildResponse(statusCode = 500, body = body)

            # Do a second lookup for all returned items to get the rest of the data
            visits = []
            for item in items:
                user_id = item['user_id']

                response = self.visits_table.get_item(
                    Key={ 'user_id': user_id }
                )

                visits.append(response['Item'])

        else:
            visits = scanTable(self.visits_table)

        body = { 'visits': visits }

        return buildResponse(statusCode = 200, body = body)

    def create_user_visit_information(self, data: dict):
        """
        Adds a new visit entry for a user to the visit information table.
        Also, emails a user if they're not registered.

        :params data: The visit entry to add.
        """

        try:
            self.validateVisitRequestBody(data)
        except InvalidRequestBody as irb:
            body = { 'errorMsg': str(irb) }
            return buildResponse(statusCode = 400, body = body)

        # Ensure no other entry with same user_id and timestamp already exists
        user_id: str = data['user_id']        
        timestamp: str = data['timestamp']
        response = self.visits_table.get_item(
            Key={
                'user_id': user_id,
                'timestamp': timestamp,
            }
        )
        if 'Item' in response:
            errorMsg: str = f"Visit entry for user {user_id} at timestamp {timestamp} already exists. Did you mean to input a different user or timestamp?"
            body = { 'errorMsg': errorMsg}
            return buildResponse(statusCode = 400, body = body)

        # Always force "_ignore" key to have value of "1"
        data['_ignore'] = "1"

        # Actually try putting the item into the table
        try:
            self.visits_table.put_item(
                Item=data
            )
        except Exception as e:
            body = { 'errorMsg': "Something went wrong on the server." }
            return buildResponse(statusCode = 500, body = body)
        
        # send user the registration link if not registered
        user_registered = self.isUserRegistered(user_id)
        if not user_registered:
            self.registrationWorkflow(user_id)

        # If here, put action succeeded. Return 201
        return buildResponse(statusCode = 201, body = {})

    def get_user_visit_information(self, user_id: str, query_parameters: dict):
        """
        Gets all of the visit information entries for a specified user from the visit information table.

        :params user_id: The name of the user.
        :params query_parameters: A dictionary of parameter names and values to filter by.
        """

        # Set the limit amount
        if 'limit' in query_parameters and query_parameters['limit'] > 0:
            limit = query_parameters['limit']
            del query_parameters['limit']
        else:
            limit = DEFAULT_QUERY_LIMIT

        if query_parameters:
            try:
                timestamp_expression = buildTimestampKeyExpression(query_parameters, 'timestamp')

            except InvalidQueryParameters as iqp:
                body = { 'errorMsg': str(iqp) }
                return buildResponse(statusCode = 400, body = body)

            try:
                key_expression = Key('user_id').eq(user_id) & timestamp_expression
                visits = queryByKeyExpression(self.visits_table, key_expression, None, limit)

            except Exception as e:
                body = { 'errorMsg': "Something went wrong on the server." }
                return buildResponse(statusCode = 500, body = body)

        else:
            key_expression = Key('user_id').eq(user_id)
            visits = queryByKeyExpression(self.visits_table, key_expression, None, limit)

        body = { 'visits': visits }

        return buildResponse(statusCode = 200, body = body)
    
    def validateVisitRequestBody(self, data: dict):
        """
        Valides the request body used when adding/updating user information.
        Will raise an InvalidRequestBody error with the details explaining
        what part of the body is invalid.

        :params data: The request body to validate.
        :raises: InvalidRequestBody
        """

        required_fields: list[str] = ["user_id", "timestamp", "location"]

        # Ensure all required fields are present
        if not allKeysPresent(required_fields, data):
            errorMsg: str = f"Missing at least one field from {required_fields} in request body."
            raise InvalidRequestBody(errorMsg)

        # Ensure timestamp is in the correct format
        try:
            datetime.strptime(data['timestamp'], TIMESTAMP_FORMAT)
        except ValueError:
            errorMsg: str = f"Timestamp not in the approved format. Approved format is 'YYYY-MM-DDThh:mm:ss'."
            raise InvalidRequestBody(errorMsg)

        # Check that the location is valid if it's still in data
        if 'location' in data:
            if data['location'] not in VALID_LOCATIONS:
                errorMsg: str = f"Specified location '{data['location']} is not one of the valid locations {VALID_LOCATIONS}'."
                raise InvalidRequestBody(errorMsg)


log_visit_function = LogVisitFunction(None, None, None)


def handler(request, context):
    # This will be hit in prod, and will connect to the stood-up dynamodb
    # and Simple Email Service clients.
    return log_visit_function.visits_handler(request, context)
