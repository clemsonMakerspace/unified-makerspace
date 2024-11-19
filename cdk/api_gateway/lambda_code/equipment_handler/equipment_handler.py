import json
from pydoc import cli
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import os
import logging
from datetime import datetime
from ..api_defaults import *

class LogEquipmentFunction():
    def __init__(self, equipment_table):
        # TODO: Setup CloudWatch Logs
        # Sets up CloudWatch logs and sets level to INFO
        # self.logger = logging.getLogger()
        # self.logger.setLevel(logging.INFO)
        
        if equipment_table is None:
            # Get the service resource.
            dynamodb = boto3.resource('dynamodb')
            # Get the table name.
            EQUIPMENT_TABLE_NAME = os.environ["EQUIPMENT_TABLE_NAME"]
            # Get table objects
            self.equipment_table = dynamodb.Table(EQUIPMENT_TABLE_NAME)
        else:
            self.equipment_table = equipment_table
            
    # Main handler function
    def equipment_handler(self, event, context):
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

            # Equipment information request handling
            if http_method == "GET" and resource_path == equipment_path:
                response = self.get_all_equipment_usage_information(query_parameters)
            elif http_method == "POST" and resource_path == equipment_path:
                response = self.create_user_equipment_usage(data)

            elif http_method == "GET" and resource_path == equipment_param_path:
                response = self.get_user_equipment_usage(user_id, query_parameters)
            elif http_method == "PATCH" and resource_path == equipment_param_path:
                response = self.patch_user_equipment_usage(user_id, data)

            return response
        except:
            errorMsg: str = f"We're sorry, but something happened. Try again later."
            body = { 'errorMsg': errorMsg }
            return buildResponse(statusCode = 500, body = body)
        
    #################################################
    # Equipment usage information function handlers #
    #################################################
    def get_all_equipment_usage_information(self, query_parameters: dict):
        """
        Returns all the equipment usage objects from the equipment usage table.

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
                items = queryByKeyExpression(self.equipment_table, key_expression, GSI = TIMESTAMP_INDEX)

            except Exception as e:
                body = { 'errorMsg': "Something went wrong on the server." }
                return buildResponse(statusCode = 500, body = body)

            # Do a second lookup for all returned items to get the rest of the data
            equipment_logs = []
            for item in items:
                user_id = item['user_id']

                response = self.equipment_table.get_item(
                    Key={ 'user_id': user_id }
                )

                equipment_logs.append(response['Item'])

        else:
            equipment_logs = scanTable(self.equipment_table)

        body = { 'equipment_logs': equipment_logs }

        return buildResponse(statusCode = 200, body = body)

    def create_user_equipment_usage(self, data: dict):
        """
        Adds an equipment usage entry for a specified user to the equipment usage table.

        :params user_id: The name of the user.
        :params data: The equipment usage entry to store.
        """

        try:
            self.validateEquipmentRequestBody(data)
        except InvalidRequestBody as irb:
            body = { 'errorMsg': str(irb) }
            return buildResponse(statusCode = 400, body = body)

        # Ensure no other entry with same user_id and timestamp already exists
        user_id: str = data['user_id']
        timestamp: str = data['timestamp']
        response = self.equipment_table.get_item(
            Key={
                'user_id': user_id,
                'timestamp': timestamp,
            }
        )
        if 'Item' in response:
            errorMsg: str = f"Equipment usage entry for user {user_id} at timestamp {timestamp} already exists. Did you mean to input a different user or timestamp?"
            body = { 'errorMsg': errorMsg}
            return buildResponse(statusCode = 400, body = body)

        # Always force "_ignore" key to have value of "1"
        data['_ignore'] = "1"

        # Actually try putting the item into the table
        try:
            self.equipment_table.put_item(
                Item=data
            )
        except Exception as e:
            body = { 'errorMsg': "Something went wrong on the server." }
            return buildResponse(statusCode = 500, body = body)

        # If here, put action succeeded. Return 201
        return buildResponse(statusCode = 201, body = {})

    def get_user_equipment_usage(self, user_id: str, query_parameters: dict = {}):
        """
        Gets all of the equipment usage objects for a specified user from the equipment usage table.

        :params user_id: The name of the user.
        :params query_parameters: A dictionary of parameter names and values to filter by.
        """

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
                equipment_logs = queryByKeyExpression(self.equipment_table, key_expression, None, limit)

            except Exception as e:
                body = { 'errorMsg': "Something went wrong on the server." }
                return buildResponse(statusCode = 500, body = body)

        else:
            key_expression = Key('user_id').eq(user_id)
            equipment_logs = queryByKeyExpression(self.equipment_table, key_expression, None, limit)

        body = { 'equipment_logs': equipment_logs }

        return buildResponse(statusCode = 200, body = body)

    def patch_user_equipment_usage(self, user_id: str, data: dict):
        """
        Updates an equipment usage entry for a specified user. Fails if no entry with a
        corresponding user_id and timetamp exists.

        :params user_id: The name of the user.
        :params data: The updated equipment usage entry.
        """

        # Ensure an entry to update actually exists
        query_parameters: dict = {
            'limit': 1
        }

        # Use a specific timestamp if provided
        if 'timestamp' in data:
            query_parameters['start_timestamp'] = data['timestamp']
            query_parameters['end_timestamp'] = data['timestamp']

        response = self.get_user_equipment_usage(user_id, query_parameters)

        statusCode = response['statusCode']
        response = json.loads(response['body'])

        # If we get request fails or there are more than one responses to work with, return 400
        if statusCode != 200 or len(response['equipment_logs']) != 1:
            errorMsg: str = f"Equipment usage logs for {user_id} could not be found. Did you mean to add a usage log?"
            body = { 'errorMsg': errorMsg }
            return buildResponse(statusCode = 400, body = body)

        else:
            equipment_log = response['equipment_logs'][0]

        # "user_id" field is never allowed for update
        if 'user_id' in data:
            errorMsg: str = "Updating the 'user_id' field is not allowed. Please remove it before trying to update user {user_id}'s information."
            body = { 'errorMsg': errorMsg }
            return buildResponse(statusCode = 400, body = body)

        # Delete the timestamp key in data if it exists before copying values
        try:
            del data['timestamp']
        except KeyError:
            pass
        
        # Ensure data['_ignore'] == '1'
        data['_ignore'] = '1'

        # Copy all all fields from data to user
        for key in data:
            equipment_log[key] = data[key]
        
        # Validate new item
        try:
            equipment_log = self.validateEquipmentRequestBody(equipment_log)
        except InvalidRequestBody as irb:
            body = { 'errorMsg': str(irb) }
            return buildResponse(statusCode = 400, body = body)

        # Try putting item back into table
        self.equipment_table.put_item(Item=equipment_log)

        # Successfully updated user
        return buildResponse(statusCode = 204, body = {})
    
    def validateEquipmentRequestBody(self, data: dict):
        """
        Valides the request body used when adding/updating equipment information.
        Removes any unnecessary keys and values from the request body.
        Will raise an InvalidRequestBody error with the details explaining
        what part of the body is invalid.

        :params data: The request body to validate.
        :returns: A valid equipment request body.
        :raises: InvalidRequestBody
        """

        required_fields: list[str] = ["user_id", "timestamp", "location",
                                    "project_name", "project_type", "equipment_type"]
        
        # Project Type Fields
        personal_project_fields = FieldCheck(
            required = [],
            disallowed = ["class_number", "faculty_name", "project_sponsor", "organization_affiliation"],
        )

        class_project_fields = FieldCheck(
            required = ["class_number", "faculty_name", "project_sponsor"],
            disallowed = ["organization_affiliation"]
        )

        club_project_fields = FieldCheck(
            required = ["organization_affiliation"],
            disallowed = ["class_number", "faculty_name", "project_sponsor"]
        )

        project_type_field_lookup = {
            'Personal': personal_project_fields,
            'Class': class_project_fields,
            'Club': club_project_fields
        }

        valid_project_types: list[str] = [key for key in project_type_field_lookup]

        # Equipment Type Fields
        """
        Due to the lack of data collection from other equipment, the only real
        required field to check is '3d_printer_info' when the type is 'SLA Printer'
        or 'FDM 3D Printer'. Otherwise, just make sure that the '3d_printer_info'
        field is disallowed for all other types. In the future, split equipment
        type fields into more specificly defined ones as needed.
        """
        printer_3d_fields = FieldCheck(
            required = ["3d_printer_info"],
            disallowed = []
        )

        other_equipment_type_fields = FieldCheck(
            required = [],
            disallowed = ["3d_printer_info"]
        )

        equipment_type_field_lookup: dict = {
            "FDM 3D Printer": printer_3d_fields, 
            "SLA Printer": printer_3d_fields, 
            "Laser Engraver": other_equipment_type_fields, 
            "Glowforge": other_equipment_type_fields, 
            "Fabric Printer": other_equipment_type_fields, 
            "Vinyl Cutter": other_equipment_type_fields, 
            "Button Maker": other_equipment_type_fields, 
            "3D Scanner": other_equipment_type_fields, 
            "Hand Tools": other_equipment_type_fields, 
            "Sticker Printer": other_equipment_type_fields, 
            "Embroidery Machine": other_equipment_type_fields, 
        }

        valid_equipment_types: list[str] = [key for key in equipment_type_field_lookup]

        # Used to check contents of '3d_printer_info' object
        equipment_3d_printer_info_fields: list[str] = ["printer_name", "print_duration",
                                                "print_mass", "print_mass_estimate",
                                                "print_status", "print_notes"]

        # Ensure all required fields are present
        if not allKeysPresent(required_fields, data):
            errorMsg: str = f"Missing at least one field from {required_fields} in request body."
            raise InvalidRequestBody(errorMsg)

        # Error if project_type is not one of the defined ones
        project_type: str = data['project_type']
        if project_type not in project_type_field_lookup:
            errorMsg: str = f"project_type {project_type} is not one of the valid project types {valid_project_types}."
            raise InvalidRequestBody(errorMsg)

        # Error if equipment_type is not one of the defined ones
        equipment_type: str = data['equipment_type']
        if equipment_type not in equipment_type_field_lookup:
            errorMsg: str = f"equipment_type {equipment_type} is not one of the valid equipment types {valid_equipment_types}."
            raise InvalidRequestBody(errorMsg)

        # Check for and clean fields related to 'project_type'
        checking_fields = project_type_field_lookup[project_type]
        try:
            data = checkAndCleanRequestFields(data, checking_fields)
        except InvalidRequestBody:
            # Re-raise InvalidRequestBody if the exception occurs
            errorMsg: str = f"Missing at least one field from {checking_fields.required} for a project_type value of '{project_type}'."
            raise InvalidRequestBody(errorMsg)

        # Check for and clean fields related to 'equipment_type'
        checking_fields = equipment_type_field_lookup[equipment_type]
        try:
            data = checkAndCleanRequestFields(data, checking_fields)
        except InvalidRequestBody:
            # Re-raise InvalidRequestBody if the exception occurs
            errorMsg: str = f"Missing at least one field from {checking_fields.required} for a equipment_type value of '{equipment_type}'."
            raise InvalidRequestBody(errorMsg)

        # Ensure 3d_printer_info object has all required fields if it is in data
        if '3d_printer_info' in data and not \
            allKeysPresent(equipment_3d_printer_info_fields, data['3d_printer_info']):

                errorMsg: str = f"Missing at least one field from {equipment_3d_printer_info_fields} in the '3d_printer_info' object in the request body."
                raise InvalidRequestBody(errorMsg)

        # Ensure timestamp is in the correct format
        try:
            datetime.strptime(data['timestamp'], TIMESTAMP_FORMAT)
        except ValueError:
            errorMsg: str = f"Timestamp not in the approved format. Approved format is 'YYYY-MM-DDThh:mm:ss'."
            raise InvalidRequestBody(errorMsg)
        
        return data

            
log_equipment_function = LogEquipmentFunction(None)

def handler(request, context):
    return log_equipment_function.equipment_handler(request, context)