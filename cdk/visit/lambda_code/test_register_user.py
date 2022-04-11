from register_user.register_user import RegisterUserFunction
from responses import mock
import pytest
import os
import json
import boto3
from moto import mock_dynamodb2

from test_utils.test_functions import create_test_users_table, create_original_table, create_test_visit_table, create_ses_client

test_register_user = {"body": json.dumps({
    "username": "jmdanie234",
    "firstName": "John",
    "lastName": "Doe",
    "Gender": "Male",
    "DOB": "01/02/2002",
    "Grad_Date": "05/01/2023",
    "Major": ["Mathematical Sciences"],
    "Minor": ["Business Administration"]
})}


@mock_dynamodb2
def test_visit_with_location():
    table = create_original_table()
    users_table = create_test_users_table()

    response = RegisterUserFunction(
        table, users_table).handle_register_user_request(test_register_user, None)
    assert response['statusCode'] == 200
