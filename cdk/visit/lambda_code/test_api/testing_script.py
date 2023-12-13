import os
import logging
from botocore.vendored import requests
import boto3
from datetime import datetime
import json
import urllib3
import time

env = os.environ["ENV"]

http = urllib3.PoolManager()

# Setting up endpoints based on stage
frontend_url = ""
api_url = ""

if env == "Beta":
    frontend_url = "https://beta-visit.cumaker.space/"
    api_url = "https://beta-api.cumaker.space/"
elif env == "Prod":
    frontend_url = "https://visit.cumaker.space/"
    api_url = "https://api.cumaker.space/"
else:
    raise Exception("Couldn't find Stage")

    # Simulates "curl <makerspace_frontend_url> | grep Makerspace Visitor Console" command
frontend_response = http.request('GET', str(frontend_url))

if frontend_response.status != 200:
    raise Exception("Front End Curl Failed")


if frontend_response.data.find(b"Makerspace Visitor Console") == -1:
    raise Exception("HTML from Front End Error")

now = datetime.now()
dt_string = now.strftime("%d-%m-%Y_%H:%M:%S")

# Triggers ttl removal 2 minutes in future
unix_timestamp_for_ttl = int(time.time()+120)

# testing visit api endpoint
visit_data = {"username": "PIPELINE_TEST_"+dt_string, "location": "Watt Family Innovation Center",
              "tool": "Visiting", "last_updated": (unix_timestamp_for_ttl)}
visit_data = json.dumps(visit_data)

visit_data_unregistered = {"username": "PIPELINE_TEST_UNREGISTERED"+dt_string,
                           "location": "Watt Family Innovation Center", "tool": "Visiting", "last_updated": (unix_timestamp_for_ttl)}
visit_data_unregistered = json.dumps(visit_data_unregistered)

visit_response = http.request('POST', str(api_url)+"visit", body=visit_data)
visit_response_unregistered = http.request(
    'POST', str(api_url)+"visit", body=visit_data_unregistered)

if visit_response.status != 200 or visit_response_unregistered.status != 200:
    raise Exception("Visit API Call Failed")

# testing register api endpoint
register_data = {
    "username": "PIPELINE_TEST_"+dt_string,
    "firstName": "TEST",
    "lastName": "USER",
    "Gender": "Male",
    "DOB": "01/01/2000",
    "UserPosition": "Undergraduate Student",
    "GradSemester": "Fall",
    "GradYear": "2023",
    "Major": ["Mathematical Sciences"],
    "Minor": ["Business Administration"],
    "last_updated": (unix_timestamp_for_ttl)
}

register_data = json.dumps(register_data)

reg_response = http.request('POST', str(
    api_url)+"register", body=register_data)

if reg_response.status != 200:
    raise Exception("Register API Call Failed")

# testing quiz Post request
quiz_data_dict = {
    "quiz_id": "3dPrinterTesting",
    "email": "CANARY_TEST_" + dt_string + "@clemson.edu",
    "score": "10 / 10",
    "last_updated": (unix_timestamp_for_ttl),
}

quiz_data = json.dumps(quiz_data_dict)

quiz_post_response = http.request(
    'POST', str(api_url) + "quiz", body=quiz_data)

if quiz_post_response.status != 200:
    raise Exception("quiz post response API Call Failed")

# testing quiz_get

quiz_data_dict_1 = {
    "quiz_id": "3dPrinterTesting1",
    "email": "CANARY_TEST_"+dt_string + "@clemson.edu",
    "score": "10 / 10",
    "last_updated": (unix_timestamp_for_ttl),
}
quiz_data_dict_2 = {
    "quiz_id": "3dPrinterTesting2",
    "email": "CANARY_TEST_"+dt_string + "@clemson.edu",
    "score": "10 / 10",
    "last_updated": (unix_timestamp_for_ttl),
}
quiz_data_dict_3 = {
    "quiz_id": "3dPrinterTesting3",
    "email": "CANARY_TEST_"+dt_string + "@clemson.edu",
    "score": "5 / 10",
    "last_updated": (unix_timestamp_for_ttl),
}

username = "CANARY_TEST_" + dt_string

quiz_post_response_1 = http.request(
    'POST', str(api_url) + "quiz", body=json.dumps(quiz_data_dict_1))
quiz_post_response_2 = http.request(
    'POST', str(api_url) + "quiz", body=json.dumps(quiz_data_dict_2))
quiz_post_response_3 = http.request(
    'POST', str(api_url) + "quiz", body=json.dumps(quiz_data_dict_3))

quiz_get_response = http.request(
    'GET', str(api_url) + "quiz/" + username)

expected_response = [
    {"quiz_id": "3dPrinterTesting1", "state": 1},
    {"quiz_id": "3dPrinterTesting2", "state": 1},
    {"quiz_id": "3dPrinterTesting3", "state": 0}
]

quiz_progress = json.loads(quiz_get_response.data)

if quiz_get_response.status != 200:
    raise Exception("quiz get response API Call Failed")

quizProgressTest = expected_response[0] in quiz_progress and expected_response[
    1] in quiz_progress and expected_response[2] in quiz_progress

responses = visit_response.status == 200 and reg_response.status == 200 and frontend_response.status == 200 and quiz_post_response.status == 200 and quiz_get_response.status == 200

print(responses and quizProgressTest)
