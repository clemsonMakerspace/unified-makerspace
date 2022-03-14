from register_user.register_user import RegisterUserFunction
from responses import mock
import pytest
import os
import json
import boto3
from moto import mock_dynamodb2


test_register_user = {"body": json.dumps({
    "username": "jmdanie234",
    "first_name": "John",
    "last_name": "Doe",
    "gender": "Male",
    "date_of_birth": "01/02/2002",
    "grad_date": "05/01/2023",
    "major": "Mathematical Sciences",
    "minor": "Business Administration"
})}


def create_dynamodb_table():
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


@mock_dynamodb2
def test_visit_with_location():
    table = create_dynamodb_table()
    response = RegisterUserFunction(
        table).handle_register_user_request(test_register_user, None)
    assert response['statusCode'] == 200
