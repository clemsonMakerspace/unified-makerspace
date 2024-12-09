import json
import boto3
from boto3.dynamodb.conditions import Key
import os
import logging
from ..api_defaults import *

class UsersHandler():
    """
    This class wraps the functionality of the lambda so we can more easily test
    it with moto. In production, we will continue to pass the stood-up
    dynamodb table to the handler itself. However, when initializing this class,
    we can choose to instead initialize it with a mocked version of the
    dynamodb table.
    """

    def __init__(self, users_table):
        # TODO: Setup CloudWatch Logs
        # Sets up CloudWatch logs and sets level to INFO
        # self.logger = logging.getLogger()
        # self.logger.setLevel(logging.INFO)
        
        if users_table is None:
            dynamodbresource = boto3.resource('dynamodb', region_name="us-east-1")
            self.USERS_TABLE_NAME = os.environ["USERS_TABLE_NAME"]
            self.users_table = dynamodbresource.Table(self.USERS_TABLE_NAME)
        else:
            self.users_table = users_table
            
    # Main handler function
    def handle_event(self, event, context):
        try:
            method_requires_body: list = ["POST", "PATCH"]

            response = buildResponse(statusCode = 400, body = {})
            http_method: str = event.get("httpMethod")
            resource_path: str = event.get("resource")

            # Get a user_id if needed
            user_id: str = ""
            if user_endpoint in resource_path:
                user_id = event['pathParameters'].get('user_id')

                # Ensure user_id is just the username if it is an email
                user_id.split('@')[0]

            # Get the body data if needed
            data: dict = {}
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

            # User information request handling
            if http_method == "GET" and resource_path == users_path:
                response = self.get_all_user_information(query_parameters)
            elif http_method == "POST" and resource_path == users_path:
                response = self.create_user_information(data)

            elif http_method == "GET" and resource_path == users_param_path:
                response = self.get_user_information(user_id)
            elif http_method == "PATCH" and resource_path == users_param_path:
                response = self.patch_user_information(user_id, data)

            return response
        except Exception as e:
            #errorMsg: str = f"We're sorry, but something happened. Try again later."
            errorMsg = str(e)
            body = { 'errorMsg': errorMsg }
            return buildResponse(statusCode = 500, body = body)
        
    ######################################
    # User information function handlers #
    ######################################
    def get_all_user_information(self, query_parameters: dict = {}):
        """
        Returns all user information entries from the user information table.

        :params query_parameters: A dictionary of parameter names and values to filter by.
        """

        # Try to get the number of items to return
        if "limit" in query_parameters:
            limit = query_parameters["limit"]

        # Otherwise return as many as possible
        else:
            limit = QUERY_LIMIT_RETURN_ALL

        users = scanTable(self.users_table, limit = limit)

        body = { 'users': users }

        return buildResponse(statusCode = 200, body = body)

    def create_user_information(self, data: dict):
        """
        Adds a new user to the user information table.

        :params data: The user information to store.
        """

        try:
            data = self.validateUserRequestBody(data)
        except InvalidRequestBody as irb:
            body = { 'errorMsg': str(irb) }
            return buildResponse(statusCode = 400, body = body)

        # Check to make sure the user doesn't already exist. Return 400 if user does exist.
        user_id: str = data['user_id']
        response = self.get_user_information(user_id)
        if response['statusCode'] == 200:
            errorMsg: str = f"User {user_id} information already exists. Did you mean to update?"
            body = { 'errorMsg': errorMsg }
            return buildResponse(statusCode = 400, body = body)

        # Actually try putting the item into the table
        try:
            self.users_table.put_item(
                Item=data
            )
        except Exception as e:
            body = { 'errorMsg': "Something went wrong on the server." }
            return buildResponse(statusCode = 500, body = body)

        # If here, put action succeeded. Return 201
        return buildResponse(statusCode = 201, body = {})

    def get_user_information(self, user_id: str):
        """
        Gets all of the information for the specified user.

        :params user_id: The name of the user.
        """

        response = self.users_table.get_item(
                Key={ 'user_id': user_id }
        )

        # user_id doesn't exist if 'Item' not in response
        if 'Item' not in response:
            errorMsg: str = f"No information for the user {user_id} could be found. Is there a typo?"
            body = { 'errorMsg': errorMsg }
            return buildResponse(statusCode = 400, body = body)

        user = response['Item']

        return buildResponse(statusCode = 200, body = user)

    def patch_user_information(self, user_id: str, data: dict):
        """
        Updates an existing user's information. Fails if the user does not exist.

        :params user_id: The name of the user.
        :params data: The updated user information.
        """

        # Ensure an entry to update actually exists
        response = self.get_user_information(user_id)
        if response['statusCode'] != 200:
            errorMsg: str = f"User {user_id} could not be found. Did you mean to add the user?"
            body = { 'errorMsg': errorMsg }
            return buildResponse(statusCode = 400, body = body)

        else:
            # Load the json object stored in response['body']
            user = json.loads(response['body'])

        # "user_id" field is never allowed for update
        if 'user_id' in data:
            errorMsg: str = "Updating the 'user_id' field is not allowed. Please remove it before trying to update user {user_id}'s information."
            body = { 'errorMsg': errorMsg }
            return buildResponse(statusCode = 400, body = body)

        # Copy all all fields from data to user
        for key in data:
            user[key] = data[key]
        
        # Validate new item
        try:
            user = self.validateUserRequestBody(user)
        except InvalidRequestBody as irb:
            body = { 'errorMsg': str(irb) }
            return buildResponse(statusCode = 400, body = body)

        # Try putting item back into table
        self.users_table.put_item(Item=user)

        # Successfully updated user
        return buildResponse(statusCode = 204, body = {})
    
    def validateUserRequestBody(self, data: dict):
        """
        Valides the request body used when creating a user information entry.
        Removes any unnecessary keys and values from the request body.
        Will raise an InvalidRequestBody error with the details explaining
        what part of the body is invalid.

        :params data: The request body to validate.
        :returns: A valid user request body.
        :raises: InvalidRequestBody
        """

        required_fields: list[str] = ["user_id", "university_status"]

        # Define required and disallowed fields for checking
        undergrad_fields = FieldCheck(required = ["undergraduate_class", "major"],
                                    disallowed = []
        )

        grad_fields = FieldCheck(required = ["major"],
                                disallowed = ["undergraduate_class"]
        )

        faculty_fields = FieldCheck(required = [],
                                    disallowed = ["undergraduate_class", "major"]
        )

        fields_lookup: dict = {
            'Undergraduate': undergrad_fields,
            'Graduate': grad_fields,
            'Faculty': faculty_fields,
        }

        valid_undergraduate_classes: list[str] = ["Freshman", "Sophomore", "Junior", "Senior"]

        # Ensure all required fields are present
        if not allKeysPresent(required_fields, data):
            errorMsg: str = f"Missing at least one field from {required_fields} in request body."
            raise InvalidRequestBody(errorMsg)

        # Error if university_status is not one of the defined ones
        university_status: str = data['university_status']
        if university_status not in fields_lookup:
            valid_statuses: list[str] = [key for key in fields_lookup]
            errorMsg: str = f"The provided university_status ('{university_status}') is not one of the valid statuses ({valid_statuses})."
            raise InvalidRequestBody(errorMsg)

        # Check for and clean fields related to 'university_status'
        checking_fields = fields_lookup[university_status]
        try:
            data = checkAndCleanRequestFields(data, checking_fields)
        except InvalidRequestBody:
            # Re-raise InvalidRequestBody if the exception occurs
            errorMsg: str = f"Missing at least one field from {checking_fields.required} due to a 'university_status' value of '{university_status}' in request body."
            raise InvalidRequestBody(errorMsg)
        
        # Check that the undergraduate class is valid if it's still in data
        if 'undergraduate_class' in data:
            if data['undergraduate_class'] not in valid_undergraduate_classes:
                errorMsg: str = f"Specified undergraduate_class ('{data['undergraduate_class']}') is not one of the valid classes {valid_undergraduate_classes} in request body."
                raise InvalidRequestBody(errorMsg)
        return data


def handler(request, context):
    # Register user information from the makerspace/register console
    # Since this will be hit in prod, it will go ahead and hit our prod
    # dynamodb table
    user_handler = UsersHandler(users_table = None)
    return user_handler.handle_event(request, context)
