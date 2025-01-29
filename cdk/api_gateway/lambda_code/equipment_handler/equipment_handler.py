import json
from pydoc import cli
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import os
import logging
from datetime import datetime
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from api_defaults import *

# Equipment Types
EQUIPMENT_NAMES: dict = {
    "FDM_PRINTER_STRING": "FDM 3D Printer (Plastic)",
    "SLA_PRINTER_STRING": "SLA Printer (Resin)",
    "LASER_ENGRAVER_STRING": "Laser Engraver",
    "GLOWFORGE_STRING": "Glowforge",
    "FABRIC_PRINTER_STRING": "Fabric Printer",
    "VINYL_CUTTER_STRING": "Vinyl Cutter",
    "BUTTON_MAKER_STRING": "Button Maker",
    "3D_SCANNER_STRING": "3D Scanner",
    "HAND_TOOLS_STRING": "Hand Tools",
    "STICKER_PRINTER_STRING": "Sticker Printer",
    "EMBROIDERY_STRING": "Embroidery Machine",
}

class EquipmentHandler():
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

            # Get the number of items to return
            if "limit" in query_parameters:
                limit = query_parameters["limit"]

            # Otherwise return as many as possible
            else:
                limit = QUERY_LIMIT_RETURN_ALL

            try:
                if timestamp_expression:
                    key_expression = Key(GSI_ATTRIBUTE_NAME).eq("1") & timestamp_expression
                else:
                    key_expression = Key(GSI_ATTRIBUTE_NAME).eq("1")

                items = queryByKeyExpression(self.equipment_table, key_expression,
                                             GSI = TIMESTAMP_INDEX, limit = limit)

            except Exception as e:
                body = { 'errorMsg': "Something went wrong on the server." }
                return buildResponse(statusCode = 500, body = body)

            # Do a second lookup for all returned items to get the rest of the data
            equipment_logs = []
            for item in items:
                user_id = item['user_id']
                timestamp = item['timestamp']

                response = self.equipment_table.get_item(
                    Key={ 
                        'user_id': user_id,
                        'timestamp': timestamp
                    }
                )

                equipment_logs.append(response['Item'])

        else:
            equipment_logs = scanTable(self.equipment_table, limit = SCAN_LIMIT_RETURN_ALL)

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

        # Always force GSI_ATTRIBUTE_NAME key to have value of "1"
        data[GSI_ATTRIBUTE_NAME] = "1"

        # Make sure "print_mass" field at least exists
        if "print_mass" not in data:
            data["print_mass"] = ""

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

        if query_parameters:
            try:
                timestamp_expression = buildTimestampKeyExpression(query_parameters, 'timestamp')

            except InvalidQueryParameters as iqp:
                body = { 'errorMsg': str(iqp) }
                return buildResponse(statusCode = 400, body = body)

            # Get the number of items to return
            if "limit" in query_parameters:
                limit = query_parameters["limit"]

            # Otherwise return as many as possible
            else:
                limit = QUERY_LIMIT_RETURN_ALL

            try:
                if timestamp_expression:
                    key_expression = Key('user_id').eq(user_id) & timestamp_expression
                else:
                    key_expression = Key('user_id').eq(user_id)

                equipment_logs = queryByKeyExpression(self.equipment_table, key_expression,
                                                      GSI = None, limit = limit)

            except Exception as e:
                body = { 'errorMsg': "Something went wrong on the server." }
                return buildResponse(statusCode = 500, body = body)

        else:
            key_expression = Key('user_id').eq(user_id)
            equipment_logs = queryByKeyExpression(
                    self.equipment_table,
                    key_expression,
                    GSI = None,
                    limit = QUERY_LIMIT_RETURN_ALL
            )

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
        
        # Ensure data[GSI_ATTRIBUTE_NAME] == '1'
        data[GSI_ATTRIBUTE_NAME] = '1'

        # Make sure "print_mass" field at least exists
        if "print_mass" not in data:
            data["print_mass"] = ""

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

        # Equipment required fields
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
        required field to check is 'printer_3d_info' when the type is 'SLA Printer'
        or 'FDM 3D Printer'. Otherwise, just make sure that the 'printer_3d_info'
        field is disallowed for all other types. In the future, split equipment
        type fields into more specificaly defined ones as needed.
        """

        printer_3d_fields = FieldCheck(
            required = ["printer_3d_info"],
            disallowed = [] # intentionally left blank to not delete other fields
        )

        other_equipment_type_fields = FieldCheck(
            required = [],
            disallowed = ["printer_3d_info"]
        )

        # Lookup dictionary to retrieve the appropriate FieldCheck object
        required_equipment_field_check_lookup: dict = {
            EQUIPMENT_NAMES["FDM_PRINTER_STRING"]: printer_3d_fields,
            EQUIPMENT_NAMES["SLA_PRINTER_STRING"]: printer_3d_fields,
            "Other": other_equipment_type_fields,
        }

        # Ensure all required fields are present
        if not allKeysPresent(required_fields, data):
            errorMsg: str = f"Missing at least one field from {required_fields} in request body."
            raise InvalidRequestBody(errorMsg)

        # Error if project_type is not one of the defined ones
        project_type: str = data['project_type']
        if project_type not in project_type_field_lookup:
            errorMsg: str = f"project_type {project_type} is not one of the valid project types {valid_project_types}."
            raise InvalidRequestBody(errorMsg)

        # Set equipment_type to "Other" if it doesn't require field checks
        equipment_type: str = data['equipment_type']
        if equipment_type not in required_equipment_field_check_lookup:
            equipment_type = "Other"

        # Check for and clean fields related to 'project_type'
        checking_fields = project_type_field_lookup[project_type]
        try:
            data = checkAndCleanRequestFields(data, checking_fields)
        except InvalidRequestBody:
            # Re-raise InvalidRequestBody if the exception occurs
            errorMsg: str = f"Missing at least one field in request body from {checking_fields.required} for a project_type value of '{project_type}'."
            raise InvalidRequestBody(errorMsg)

        # Check for and clean fields related to 'equipment_type'
        checking_fields = required_equipment_field_check_lookup[equipment_type]
        try:
            data = checkAndCleanRequestFields(data, checking_fields)
        except InvalidRequestBody:
            # Re-raise InvalidRequestBody if the exception occurs
            errorMsg: str = f"Missing at least one field in request body from {checking_fields.required} for an equipment_type value of '{equipment_type}'."
            raise InvalidRequestBody(errorMsg)

        # Ensure printer_3d_info object has all required fields if it is in data
        # General required fields all 'printer_3d_info' objects are required to have
        general_printer_3d_info_fields: list[str] = ["printer_name", "print_name", "print_duration",
                                                     "print_status", "print_notes"]
        # Required fields specific to FDM 3D Printers
        fdm_printer_3d_required_fields: list[str] = ["print_mass_estimate"] + general_printer_3d_info_fields

        # Required fields specific to SLA 3D Printers
        sla_printer_3d_required_fields: list[str] = ["resin_volume", "resin_type"] + general_printer_3d_info_fields

        # Check FDM printer fields
        if data["equipment_type"] == EQUIPMENT_NAMES["FDM_PRINTER_STRING"] and not \
            allKeysPresent(fdm_printer_3d_required_fields, data['printer_3d_info']):

                errorMsg: str = f"Missing at least one field in 'printer_3d_info' object from {fdm_printer_3d_required_fields} in the 'printer_3d_info' object in the request body."
                raise InvalidRequestBody(errorMsg)

        # Check SLA printer fields
        elif data["equipment_type"] == EQUIPMENT_NAMES["SLA_PRINTER_STRING"] and not \
            allKeysPresent(sla_printer_3d_required_fields, data['printer_3d_info']):

                errorMsg: str = f"Missing at least one field in 'printer_3d_info' object from {fdm_printer_3d_required_fields} in the 'printer_3d_info' object in the request body."
                raise InvalidRequestBody(errorMsg)


        # Ensure timestamp is in the correct format
        try:
            datetime.strptime(data['timestamp'], TIMESTAMP_FORMAT)
        except ValueError:
            errorMsg: str = f"Timestamp not in the approved format. Approved format is 'YYYY-MM-DDThh:mm:ss'."
            raise InvalidRequestBody(errorMsg)
        
        return data

            

def handler(request, context):
    equipment_handler = EquipmentHandler(None)
    return equipment_handler.handle_event(request, context)
