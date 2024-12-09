import json
from pydoc import cli
import boto3
import logging
from ..api_defaults import *

class TigerTrainingHandler():
    def __init__(self):
        # Sets up CloudWatch logs and sets level to INFO
        # self.logger = logging.getLogger()
        # self.logger.setLevel(logging.INFO)
        pass
        
    # Main handler function
    def handle_event(self, event, context):
        """ 
        Handles the request of what the user is trying accomplish with any endpoint regarding qualifications.
        Based on the request, it will route to the appropriate function to accomplish the request.
        Performs validation checks and creates return responses based on success/fail.
        """
        try:
            response = buildResponse(statusCode = 400, body = {})

            # Pull and store tiger training data regardless of method
            response = self.call_tiger_training_pull()

            return response

        except:
            errorMsg: str = f"We're sorry, but something happened. Try again later."
            body = { 'errorMsg': errorMsg }
            return buildResponse(statusCode = 500, body = body)
            
    ############################################
    # Tiger Training Data Collection Functions #
    ############################################
    def call_tiger_training_pull(self):
        """
        
        """
            

def handler(request, context):
    tiger_training_handler = TigerTrainingHandler()
    return tiger_training_handler.handle_event(request, context)
