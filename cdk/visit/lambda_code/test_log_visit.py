from log_visit import *
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    assertions
)
from moto import mock_dynamodb2
import pytest


test_log_visit_with_no_location = {
    "body": "{\"username\":\"jmdanie234\"}"
}

test_log_visit_with_location = {
    "body": "{\"username\":\"jmdanie234\",\"location\":\"Watt Location\"}"
}


@mock_dynamodb2
def test_lambda_handler():
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

    """
    log_visit_lambda = _lambda.Function(
        self,
        'LogVisit',
        runtime=_lambda.Runtime.PYTHON_3_7,
        handler='index.handler',
        code=_lambda.Code.asset('log_visit'),
        environment={
            'TABLE_NAME': table_name
        }
    )

    # Add the Lambda Permission so that the log_visit_lambda can invoke
    # the addVisitEntry function.
    log_visit_lambda.add_permission(
        'LogVisitPermission',
        principal=_lambda.ServicePrincipal('logs.amazonaws.com'),
        source_arn=log_visit_lambda.function_arn,
        action_names=['lambda:InvokeFunction']
    )

    # Create a new SES resource and specify a region.
    client = boto3.client('ses', region_name='us-east-1')

    # Try to send the email.
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': ['


    stack=Stack()
    """
    try:
        response = lambda_handler(test_log_visit_with_no_location, None)
        assert response['statusCode'] == 200
    except Exception as e:
        print(e)
