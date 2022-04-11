import boto3


def create_test_users_table():
    table_name = 'users'
    dymanodb = boto3.resource('dynamodb', 'us-east-1')

    table = dymanodb.create_table(
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


def create_test_visit_table():
    """
    Create a dynamodb table for testing

    Returns:
        dynamodb.Table: A dynamodb table

    """
    table_name = 'visits'
    dymanodb = boto3.resource('dynamodb', 'us-east-1')

    table = dymanodb.create_table(
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
                'AttributeType': 'S'
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


def create_original_table():
    table_name = 'ORIGINAL'
    dymanodb = boto3.resource('dynamodb', 'us-east-1')

    table = dymanodb.create_table(
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
