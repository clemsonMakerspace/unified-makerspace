import boto3


def create_dynamodb_client():

    return boto3.client('dynamodb', 'us-east-1')


def create_test_users_table(client):
    table_name = 'users'
    resource = boto3.resource('dynamodb', region_name='us-east-1')

    table = resource.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'username',
                'KeyType': 'HASH'  # Partition key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'username',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    table.wait_until_exists()

    return table


def create_test_visit_table(client):
    """
    Create a dynamodb table for testing

    Returns:
        dynamodb.Table: A dynamodb table

    """
    table_name = 'visits'

    resource = boto3.resource('dynamodb', region_name='us-east-1')
    table = resource.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'visit_time',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'username',
                'KeyType': 'RANGE'  # Sort key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'visit_time',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'username',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    table.wait_until_exists()

    return table


def create_ses_client():
    client = boto3.client('ses', region_name='us-east-1')

    return client


def create_original_table(client):
    table_name = 'ORIGINAL'

    resource = boto3.resource('dynamodb', region_name='us-east-1')
    table = resource.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'PK',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'SK',
                'KeyType': 'RANGE'  # Sort key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'PK',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'SK',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    table.wait_until_exists()

    return table
