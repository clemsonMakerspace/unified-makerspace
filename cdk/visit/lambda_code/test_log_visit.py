from moto import mock_dynamodb2, mock_ses
import boto3
import pytest
import os

os.environ["TABLE_NAME"] = "visits"
os.environ["AWS_REGION"] = "us-east-1"

# This has to run after we set the environment variables
# so we don't break pytest.
from log_visit.log_visit import LogVisitFunction


test_log_visit_with_no_location = {
    "body": "{\"username\":\"jmdanie234\"}"
}

test_log_visit_with_location = {
    "body": "{\"username\":\"jmdanie234\",\"location\":\"Watt Location\"}"
}


def create_dynamodb_table():
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
                'AttributeName': 'PK',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'SK',
                'KeyType': 'RANGE'  # Sort key
            },
            {
                'AttributeName': 'location',
                'KeyType': 'RANGE'
            }
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
            {
                'AttributeName': 'location',
                'AttributeType': 'S'
            }
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


@mock_dynamodb2
@mock_ses
def test_visit_with_location():
    table = create_dynamodb_table()
    client = create_ses_client()

    response = LogVisitFunction(table, client).handle_log_visit_request(
        test_log_visit_with_location, None)
    assert response['statusCode'] == 200


@mock_dynamodb2
def test_visit_with_no_location():
    table = create_dynamodb_table()
    response = LogVisitFunction(table, None).handle_log_visit_request(
        test_log_visit_with_no_location, None)
    assert response['statusCode'] == 200
