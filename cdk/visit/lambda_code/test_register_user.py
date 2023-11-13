from register_user.register_user import RegisterUserFunction
from responses import mock
import pytest
import os
import json
import boto3
from moto import mock_dynamodb2

from test_utils.test_functions import *

test_register_user = {"body": json.dumps({
    "username": "jmdanie234",
    "firstName": "John",
    "lastName": "Doe",
    "Gender": "Male",
    "DOB": "01/02/2002",
    "UserPosition": "Undergraduate Student",
    "GradSemester": "Fall",
    "GradYear": "2023",
    "Major": ["Mathematical Sciences"],
    "Minor": ["Business Administration"]
})}


@mock_dynamodb2
def test_visit_with_location():
    client = create_dynamodb_client()
    users_table = create_test_users_table(client)

    response = RegisterUserFunction(
        users_table, client).handle_register_user_request(test_register_user, None)
    assert response['statusCode'] == 200
