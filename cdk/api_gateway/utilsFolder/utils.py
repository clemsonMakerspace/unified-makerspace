# from ....api_gateway.lambda_code.api_defaults import
from ..lambda_code.api_defaults import *
from moto import mock_aws
import boto3


@mock_aws
def create_table(table_name: str, primary_key: str):
    """
    Create a dynamodb table to use when testing.

    :params table_name: The name of the dynamodb table.
    :params primary_key: The name of the primary key.
    :returns: A dynamodb.Table to use.
    """

    boto3.setup_default_session()
    resource = boto3.resource('dynamodb', region_name='us-east-1')
    created_table = resource.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': primary_key,
                'KeyType': 'HASH'  # Partition key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': primary_key,
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    created_table.wait_until_exists()

    return resource.Table(table_name)


@mock_aws
def create_gsi_table(table_name: str, primary_key: str, sort_key: str):
    """
    Create a dynamodb table with a global secondary index to use when testing.

    :params table_name: The name of the dynamodb table.
    :params primary_key: The name of the primary key to use.
    :params sort_key: The name of the sort key to use.
    :returns: A dynamodb.Table to use.
    """

    boto3.setup_default_session()
    resource = boto3.resource('dynamodb', region_name='us-east-1')
    table = resource.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': primary_key,
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': sort_key,
                'KeyType': 'RANGE'  # Sort key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': primary_key,
                'AttributeType': 'S'
            },
            {
                'AttributeName': sort_key,
                'AttributeType': 'S'
            },
            {
                'AttributeName': GSI_ATTRIBUTE_NAME,
                'AttributeType': 'S'
            },
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': TIMESTAMP_INDEX,
                'KeySchema': [
                    {
                        'AttributeName': GSI_ATTRIBUTE_NAME,
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': sort_key,
                        'KeyType': 'RANGE'
                    },
                ],
                'Projection': {
                    'ProjectionType': 'KEYS_ONLY'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                },
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    table.wait_until_exists()

    return table


@mock_aws
def create_ses_client():
    boto3.setup_default_session()
    client = boto3.client('ses', region_name='us-east-1')

    return client


def create_rest_http_event(httpMethod: str, resource: str,
                      body = {},
                      pathParameters: dict = {},
                      queryStringParameters: dict = {}
                      ) -> dict:
    """
    Creates a Rest HTTP event similar to what ApiGateway will
    send to a lambda proxy. Use to simulate an event an api
    handler would receive and handle.

    :params httpMethod: The http method of the event. One of:
                        "GET", "POST", "PATCH", "PUT", and
                        "DELETE".
    :params resource: The endpoint resource of the api that will
                      be acted on. Path parameters must be named,
                      not resolved, and should be in curly
                      brackets ({}).
                      Example: /test/{test_id}
    :params body: The request json body to be sent.
    :params pathParamters: A dictionary of path parameter names and
                           their values.
    :params queryStringParameters: A dictionary of query parameter
                                   names and their values as strings.
    :returns: A json object representing an AWS ApiGateway event.
    """

    # Stringify the body
    response = locals()
    response['body'] = json.dumps(response['body'])
    return response


def jsonify_response(response: dict) -> dict:
    """
    Responses returned by the backend api have a few fields (e.g., 'body')
    as a stringified json. This function jsonifies all strigified fields.

    :params response: A response object from the backend api.
    """

    # Convert body
    response['body'] = json.loads(response['body'])
    return response


def get_all_table_items(dynamodb_table) -> dict:
    """
    Scans and returns all items found in a provided dynamodb table.

    :params dynamodb_table: The dynamodb table to scan items for.
    :returns: The dictionary { 'items': [list of all scanned items] }
    """

    # Scan for all items in the table
    items: list = scanTable(dynamodb_table)

    # Format them into a dictionary
    data: dict = { 'items': items }

    # Return the dictionary
    return data


def put_all_items_in_table(dynamodb_table, items: list):
    """
    Put all provided items into the provided table.

    :params dynamodb_table: The dynamodb table to scan items for.
    :params items: A list of dictionaries representing items to
                   add to the table.
    """

    for item in items:
        dynamodb_table.put_item(Item=item)


def print_all_table_items(dynamodb_table):
    """
    Pretty prints the contents of a dynamodb table.

    :params dynamodb_table: The dynamodb table to scan items for.
    """
    
    # Get all the table items
    data = get_all_table_items(dynamodb_table)

    # Pretty print the data
    print(f"\n\nTable Items:\n{json.dumps(data, indent=2)}")
