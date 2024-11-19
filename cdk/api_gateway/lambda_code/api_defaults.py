import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
from datetime import datetime
from dataclasses import dataclass

class InvalidQueryParameters(BaseException):
    """
    An exception that should be raised if a query parameter
    -- or combination of query parameters -- is not acceptable.
    """
    def __init__(self, *args):
        """
        Initialize the exception with a custom message. The message
        must be passed as an arg.
        """
        exceptionMsg = "One (or more) query parameters are invalid."
        if not args:
            args = (exceptionMsg,)

        # Initialize exception with args
        super().__init__(*args)

class InvalidRequestBody(BaseException):
    """
    An exception that should be raised if a request body
    does not match requirements.
    """
    def __init__(self, *args):
        """
        Initialize the exception with a custom message. The message
        must be passed as an arg.
        """
        exceptionMsg = "One (or more) required keys are missing."
        if not args:
            args = (exceptionMsg,)

        # Initialize exception with args
        super().__init__(*args)

@dataclass
class FieldCheck():
    """
    Class to be used when checking fields for a key. Comprised of string lists of
    'required' and 'disallowed' fields.
    """
    required: list[str]
    disallowed: list[str]

@dataclass
class CompletableItem():
    """
    Class used to represent items that can be completable. This class
    is hashable and can be used in sets, keys in dictionaries, etc.
    """
    name: str = ""
    completion_status: str = ""

    def __hash__(self):
        """
        Generate a hash of the class. Uses the 'name'
        class variable for hashing.
        """
        return hash((self.name))

# Define path constants
user_endpoint: str = "/{user_id}"
users_path: str = "/users"
users_param_path: str = users_path + user_endpoint
visits_path: str = "/visits"
visits_param_path: str = visits_path + user_endpoint
equipment_path: str = "/equipment"
equipment_param_path: str = equipment_path + user_endpoint
qualifications_path: str = "/qualifications"
qualifications_param_path: str = qualifications_path + user_endpoint

# Other global values
DEFAULT_SCAN_LIMIT: int = 1000
DEFAULT_QUERY_LIMIT: int = 1000
TIMESTAMP_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
TIMESTAMP_INDEX: str = "TimestampIndex"
VALID_LOCATIONS: list[str] = ["Watt", "Cooper", "CUICAR"]
VALID_QUERY_PARAMETERS: list[str] = [
    "start_timestamp",
    "end_timestamp",
    "limit"
]
INT_QUERY_PARAMETERS: list[str] = ["limit"]

def buildResponse(statusCode: int, body: dict):
    """
    Returns a valid response to return to API Gateway.

    :params statusCode: The response status code.
    :params body: The content to return in a dictionary.
    """
    return {
        "statusCode": statusCode,
		"headers": {
			"Content-Type": "application/json"
		},
        "body": json.dumps(body)
    }

def buildTimestampKeyExpression(query_parameters: dict, timestamp_attr_name: str):
    """
    Returns a valid Key() expression to use when sorting by timestamp. Use this
    value by &ing it with other KeyConditionExpressions.

    :note: The timestamp attribute MUST be a sort key. Additionally, at least one
           of the following key names must be in query_parameters with a value.
           Given query values must be in ISO 8601 format excluding the local
           offset (e.g., YYYY-MM-DDThh:mm:ss). 

           Valid Query Parameter Keys:
           start_timestamp
           end_timestamp

    :params query_parameters: The dictionary containing on of the keys
                              mention above.
    :params timestamp_attr_name: The name of the data field containing
                                 the ISO 8601 compliant (as described
                                 above in the note) timestamps.
    :raises InvalidQueryParameters: If the start_timestamp occurs after
                                    the end_timestamp
    """

    start_timestamp = None
    end_timestamp = None

    if "end_timestamp" in query_parameters:
        end_timestamp = query_parameters["end_timestamp"]
    if "start_timestamp" in query_parameters:
        start_timestamp = query_parameters["start_timestamp"]

    # Build the FilterExpression to filter by
    if end_timestamp and not start_timestamp:
        expression = Key(timestamp_attr_name).lte(end_timestamp)

    elif start_timestamp and not end_timestamp:
        expression = Key(timestamp_attr_name).gte(start_timestamp)

    elif start_timestamp == end_timestamp:
        expression = Key(timestamp_attr_name).eq(start_timestamp)

    else:
        # Can't have the end_timestamp occur before the start_timestamp
        if str(end_timestamp) < str(start_timestamp):
            raise InvalidQueryParameters("When searching with both start and end timestamps, end_timestamp cannot occur before start_timestamp.")

        expression = Key(timestamp_attr_name).between(start_timestamp, end_timestamp)

    return expression

def queryByKeyExpression(table, key_expression, GSI = None, limit = DEFAULT_QUERY_LIMIT) -> list:
    """
    Queries a given table for all entries that match the provided key
    expression. When desiring to search by timestamp, table is required
    to have a secondary global index with a primary key of {"S": "_ignore"}
    and a sort key set to the timestamp attribute name. All entries to be
    queried by timestamp must have an _ignore value of "1". Any other table
    entry with an _ignore value that isn't "1" will be ignored.

    :note: This will return a list of objects containing the values of the
           primary key of the table, the corresponding timestamp, and the
           _ignore value ("1"). Additional queries using this data may be
           needed to get more information from the table. Also, the queried
           table MUST have the timestamp field provided to the key expression
           as a sort key.
    :params table: The dynamodb.Table to scan.
    :params key_expression: A valid Key() expression to filter results by.
                            Common problems result from trying to use a
                            non primary key (primary+sort) in the expression.
    :params GSI: The string name of the global secondary index that has _ignore
                 primary key and timestamp as the sort key. Required if
                 trying to query by timestamps.
    :return: A list containing all entries that pass the timestamp filtering.
    """

    """
    Query at least once, then keep querying until queries
    stop exceeding response limit.
    """

    # TODO: Put params into an args tuple and call *args in .scan()

    # The list that will store all matching query items
    items: list = []
    try:
        if GSI != None:
            response = table.query(
                IndexName=GSI,
                KeyConditionExpression=key_expression,
                ScanIndexForward=False, # Orders results by descending timestamp
            )
        else:
            response = table.query(
                KeyConditionExpression=key_expression,
                ScanIndexForward=False, # Orders results by descending timestamp
            )

        items += response['Items']

        """
        Query until "LastEvaluatedKey" isn't in response (all appropriate keys
        where checked) or until the length of items >= limit
        """
        while "LastEvaluatedKey" in response and len(items) < limit:
            if GSI != None:
                response = table.query(
                    IndexName=GSI,
                    KeyConditionExpression=key_expression,
                    ScanIndexForward=False, # Orders results by descending timestamp
                )
            else:
                response = table.query(
                    KeyConditionExpression=key_expression,
                    ScanIndexForward=False, # Orders results by descending timestamp
                )

            items += response['Items']

    except Exception as e:
        # Don't log since this function's errors should be handled by caller
        raise Exception(e)

    return items[0:limit]

def scanTable(table, filter_expression = None) -> list:
    """
    Scans an entire dynamodb table. Optionally uses a passed in filter expression
    to limit the results returned.

    :params table: The dynamodb.Table to use.
    :params filter_expression: The optional Attr() filter to use.
    :return: A list of all returned items (that optionally match
              filter_expression).
    """

    # List to store returned items
    items: list = []

    """
    Scan at least once, then keep scanning until either no more
    items are returned or the end of the table is reached.
    """
    try:
        if not filter_expression == None:
            response = table.scan(
                FilterExpression=filter_expression,
                Limit=DEFAULT_SCAN_LIMIT
            )

        else:
            response = table.scan(
                Limit=DEFAULT_SCAN_LIMIT
            )

        items += (response['Items'])

        # Keep scanning for more items until no more return
        while 'Items' in response and 'LastEvaluatedKey' in response:
            if not filter_expression == None:
                response = table.scan(
                    FilterExpression=filter_expression,
                    Limit=DEFAULT_SCAN_LIMIT,
                    ExclusiveStartKey=response['LastEvaluatedKey']
                )

            else:
                response = table.scan(
                    Limit=DEFAULT_SCAN_LIMIT,
                    ExclusiveStartKey=response['LastEvaluatedKey']
                )

            items += (response['Items'])

    except KeyError:
        pass

    except Exception as e:
        raise e

    return items

def allKeysPresent(keys: list[str], data: dict) -> bool:
    """
    Checks if all strings in a list are in a dictionary.

    :params keys: A list of strings to check as keys for the dictionary.
    :params data: The dictionary to check the keys against.
    :returns: True if all keys are present, false if at least one of them isn't.
    """

    for key in keys:
        if key not in data:
            return False
    return True

def anyKeysPresent(keys: list[str], data: dict) -> bool:
    """
    Checks if any strings in a list are in a dictionary.

    :params keys: A list of strings to check as keys for the dictionary.
    :params data: The dictionary to check the keys against.
    :returns: True if at leasy one key is present, false if all keys are not present.
    """

    for key in keys:
        if key in data:
            return True
    return False

def checkAndCleanRequestFields(data: dict, field_check):
    """
    Checks a request body for required and disallowed fields.
    Raises an InvalidRequestBody if a required field is missing,
    and deletes any found disallowed fields.

    :params data: The request body to check.
    :params field_check: A FieldCheck object with the required
                         and disallowed fields.
    :returns: A copy of the inputted request body, but with
              disallowed fields removed.
    :raises: InvalidRequestBody
    """

    # Required field check
    for required_field in field_check.required:
        if required_field not in data:
            errorMsg: str = f"Missing at least one field from {field_check.required}."
            raise InvalidRequestBody(errorMsg)

    # Delete disallowed keys
    for disallowed_field in field_check.disallowed:
        try:
            del data[disallowed_field]
        except KeyError:
            pass
    
    return data
