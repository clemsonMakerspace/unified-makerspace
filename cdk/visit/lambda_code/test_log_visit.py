from log_visit.log_visit import LogVisitFunction
from moto import mock_dynamodb2, mock_ses
import boto3
import pytest
import os
import logging
from test_utils.test_functions import create_test_users_table, create_original_table, create_test_visit_table, create_ses_client

test_log_visit_with_no_location = {
    "body": "{\"username\":\"jmdanie234\"}"
}

test_log_visit_with_location = {
    "body": "{\"username\":\"jmdanie234\",\"location\":\"Watt\"}"
}


@mock_dynamodb2
@mock_ses
def test_visit_with_location():
    original_table = create_original_table()
    visits_table = create_test_visit_table()
    users_table = create_test_users_table()
    client = create_ses_client()

    response = LogVisitFunction(original_table, visits_table, users_table, client).handle_log_visit_request(
        test_log_visit_with_location, None)
    assert response['statusCode'] == 200


@mock_dynamodb2
def test_visit_with_no_location():
    original_table = create_original_table()
    visits_table = create_test_visit_table()
    users_table = create_test_users_table()
    response = LogVisitFunction(original_table, visits_table, users_table, None).handle_log_visit_request(
        test_log_visit_with_no_location, None)
    assert response['statusCode'] == 200
