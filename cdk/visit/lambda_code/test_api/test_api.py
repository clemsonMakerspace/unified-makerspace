
import os
import logging
from botocore.vendored import requests
import boto3
from datetime import datetime
import json
import urllib3
import time

class TestAPIFunction():
    """
    This function will be used to wrap the functionality of the lambda
    so we can more easily test with pytest.
    """

    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.env = os.environ["ENV"]


    def handle_test_api(self):
        http = urllib3.PoolManager()  

        # Setting up endpoints based on stage
        frontend_url = ""
        api_url = ""

        if self.env == "Beta":
            frontend_url = "https://beta-visit.cumaker.space/"
            api_url = "https://beta-api.cumaker.space/"
        elif self.env == "Prod":
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
        dt_string = now.strftime("%d/%m/%Y_%H:%M:%S")
        
        unix_timestamp_for_ttl = int(time.time()+120) # Triggers ttl removal 2 minutes in future 

        # testing visit api endpoint
        visit_data = {"username":"CANARY_TEST_"+dt_string,"location":"Watt Family Innovation Center","tool":"Visiting","last_updated":(unix_timestamp_for_ttl)}
        visit_data = json.dumps(visit_data)

        visit_response = http.request('POST', str(api_url)+"visit",body=visit_data)


        visit_data_unregistered = {"username":"CANARY_TEST_UNREGISTERED"+dt_string,"location":"Watt Family Innovation Center","tool":"Visiting","last_updated":(unix_timestamp_for_ttl)}
        visit_data_unregistered  = json.dumps(visit_data_unregistered )

        visit_response = http.request('POST', str(api_url)+"visit",body=visit_data)
        visit_response_unregistered = http.request('POST', str(api_url)+"visit",body=visit_data_unregistered)

        if visit_response.status != 200 or visit_response_unregistered.status != 200:
            raise Exception("Visit API Call Failed")

        # testing register api endpoint
        register_data = {
            "username": "CANARY_TEST_"+dt_string,
            "firstName": "TEST",
            "lastName": "USER",
            "Gender": "Male",
            "DOB": "01/01/2000",
            "UserPosition": "Undergraduate Student",
            "GradSemester": "Fall",
            "GradYear": "2023",
            "Major": ["Mathematical Sciences"],
            "Minor": ["Business Administration"],
            "last_updated":(unix_timestamp_for_ttl)
        }

        register_data = json.dumps(register_data)

        reg_response = http.request('POST', str(api_url)+"register",body=register_data)

        if reg_response.status != 200: 
            raise Exception("Register API Call Failed")


        return visit_response.status == 200 and reg_response.status== 200 and frontend_response.status==200
        


test_api_function = TestAPIFunction()

def handler(request, context):
    return test_api_function.handle_test_api()


