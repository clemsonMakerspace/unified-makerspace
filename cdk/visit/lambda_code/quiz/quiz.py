import json
import boto3
from boto3.dynamodb.conditions import Key
import os
import time
from typing import Tuple


class QuizFunction():
    """
    This class wraps the function of the lambda so we can more easily test
    it with moto. In production, we will continue to pass the stood-up
    dynamodb table to the handler itself. However, when initializing this class,
    we can choose to instead initialize it with a mocked version of the
    dynamodb table.
    """

    def __init__(self, quiz_list_table, quiz_progress_table, dynamodbclient):
        if dynamodbclient is None:
            self.dynamodbclient = boto3.client('dynamodb')
        else:
            self.dynamodbclient = dynamodbclient

        self.QUIZ_LIST_TABLE_NAME = os.environ["QUIZ_LIST_TABLE_NAME"]
        if quiz_list_table is None:
            dynamodbresource = boto3.resource('dynamodb')
            self.quiz_list = dynamodbresource.Table(self.QUIZ_LIST_TABLE_NAME)
        else:
            self.quiz_list = quiz_list_table

        self.QUIZ_PROGRESS_TABLE_NAME = os.environ["QUIZ_PROGRESS_TABLE_NAME"]
        if quiz_progress_table is None:
            dynamodbresource = boto3.resource('dynamodb')
            self.quiz_progress = dynamodbresource.Table(
                self.QUIZ_PROGRESS_TABLE_NAME)
        else:
            self.quiz_progress = quiz_progress_table

    def does_quiz_exist(self, quiz_id):
        """
            true if the quiz is in the quiz list
        """
        quiz_list_response = self.quiz_list.query(
            KeyConditionExpression=Key('quiz_id').eq(quiz_id)
        )
        return quiz_list_response['Count'] != 0

    def get_username(self, email):
        userName = email.split('@')

        return userName[0]

    def get_quiz_state(self, score):
        """
            input: a string like of the quiz score "9 / 10" or "3 / 3"
            return: 1 if all questions are correct and a 0 if otherwise
        """

        score = score.split('/')

        userScore = int(score[0].strip())
        totalScore = int(score[1].strip())

        if userScore == totalScore:
            return 1
        else:
            return 0

    def add_quiz_info(self, quiz_info):
        """
            Steps for adding quiz info to db:
                1. Check if quiz_id exist in quiz_list
                    - if not -> add quiz_id to quiz_list
                2. Format incoming data for db
                3. Insert quiz_info into quiz_progress_table
        """

        if not self.does_quiz_exist(quiz_info['quiz_id']):
            quiz_list_item = {
                'quiz_id': quiz_info['quiz_id']
            }
            # if the json is from a test request it will have this ttl attribute
            if "last_updated" in quiz_info:
                quiz_list_item['last_updated'] = quiz_info['last_updated']

            quiz_list_response = self.quiz_list.put_item(
                Item=quiz_list_item
            )

        timestamp = int(time.time())
        username = self.get_username(quiz_info['email'])
        state = self.get_quiz_state(quiz_info['score'])

        quiz_progress_item = {
            'quiz_id': quiz_info['quiz_id'],
            'username': username,
            'timestamp': timestamp,
            'state': state
        }

        # if the json is from a test request it will have this ttl attribute
        if "last_updated" in quiz_info:
            quiz_progress_item['last_updated'] = quiz_info['last_updated']

        quiz_progress_table_response = self.quiz_progress.put_item(
            Item=quiz_progress_item
        )

        return quiz_progress_table_response['ResponseMetadata']['HTTPStatusCode']

    def handle_quiz_request(self, request, context):
        HEADERS = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': os.environ["DOMAIN_NAME"],
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        }
        if (request is None):
            return {
                'headers': HEADERS,
                'statusCode': 400,
                'body': json.dumps({
                    "Message": "Failed to provide parameters"
                })
            }

        # Get all of the quiz information from the json file
        quiz_info = json.loads(request["body"])
        # Call Function
        response = self.add_quiz_info(quiz_info)
        # Send response
        return {
            'headers': HEADERS,
            'statusCode': response
        }


quiz_function = QuizFunction(None, None, None)


def handler(request, context):
    # Register quiz information from the makerspace/register console
    # Since this will be hit in prod, it will go ahead and hit our prod
    # dynamodb table
    return quiz_function.handle_quiz_request(
        request, context)
