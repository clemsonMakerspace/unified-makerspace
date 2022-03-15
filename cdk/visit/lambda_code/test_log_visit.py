from log_visit.log_visit import LogVisitFunction
from moto import mock_dynamodb2, mock_ses
import boto3
import pytest
import os
import logging

test_log_visit_with_no_location = {
    "body": "{\"username\":\"jmdanie234\"}"
}

test_log_visit_with_location = {
    "body": "{\"username\":\"jmdanie234\",\"location\":\"Watt\"}"
}


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
            {
                'AttributeName': 'last_name',
                'KeyType': 'RANGE'  # Sort key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'username',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'last_name',
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
            {
                'AttributeName': 'location',
                'KeyType': 'RANGE'
            }
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
    visits_table = create_test_visit_table()
    users_table = create_test_users_table()
    client = create_ses_client()

    response = LogVisitFunction(visits_table, users_table, client).handle_log_visit_request(
        test_log_visit_with_location, None)

    assert response['statusCode'] == 200


@mock_dynamodb2
def test_visit_with_no_location():
    visits_table = create_test_visit_table()
    users_table = create_test_users_table()
    response = LogVisitFunction(visits_table, users_table, None).handle_log_visit_request(
        test_log_visit_with_no_location, None)
    assert response['statusCode'] == 200
