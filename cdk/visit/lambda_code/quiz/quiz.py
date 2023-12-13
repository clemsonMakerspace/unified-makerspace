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
            self.users = dynamodbresource.Table(self.QUIZ_LIST_TABLE_NAME)
        else:
            self.quiz_list = quiz_list_table

        self.QUIZ_PROGRESS_TABLE_NAME = os.environ["QUIZ_PROGRESS_TABLE_NAME"]
        if quiz_progress_table is None:
            dynamodbresource = boto3.resource('dynamodb')
            self.users = dynamodbresource.Table(self.QUIZ_PROGRESS_TABLE_NAME)
        else:
            self.quiz_progress = quiz_progress_table

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

    def get_quiz_progress(self, username):
        """
            Steps for getting user quiz progress:
                1. Get all quiz_id's from quiz_list
                2. Retrieve all quiz entries for the user from quiz_progress
                3. Return list of all quizzes with quiz state
        """

        # Step 1
        quiz_list_response = self.quiz_list.scan()
        all_quizzes = quiz_list_response['Items']

        # Step 2
        user_quiz_states = {}
        for quiz in all_quizzes:
            quiz_id = quiz['quiz_id']
            quiz_progress_response = self.quiz_progress.query(
                KeyConditionExpression=Key('username').eq(
                    username) & Key('quiz_id').eq(quiz_id)
            )
            if quiz_progress_response['Items']:
                quiz_data = quiz_progress_response['Items'][0]
                user_quiz_states[quiz_id] = int(quiz_data['state'])
            else:
                # User has not taken this quiz
                user_quiz_states[quiz_id] = -1

        # Step 3
        user_quiz_progress = []
        for quiz in all_quizzes:
            quiz_id = quiz['quiz_id']
            quiz_info = {
                'quiz_id': quiz_id,
                'state': user_quiz_states.get(quiz_id)
            }
            user_quiz_progress.append(quiz_info)

        return user_quiz_progress

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

        method = request.get('httpMethod')

        if method == 'POST':
            quiz_info = json.loads(request["body"])
            response = self.add_quiz_info(quiz_info)
            return {
                'headers': HEADERS,
                'statusCode': response
            }
        elif method == 'GET':
            username = request.get('pathParameters', {}).get('username')
            if not username:
                return {
                    'headers': HEADERS,
                    'statusCode': 400,
                    'body': json.dumps({
                        "Message": "Username parameter is missing"
                    })
                }

            user_quiz_progress = self.get_quiz_progress(username)
            return {
                'headers': HEADERS,
                'statusCode': 200,
                'body':  json.dumps(user_quiz_progress)
            }
        else:
            return {
                'headers': HEADERS,
                'statusCode': 405,
                'body': json.dumps({
                    "Message": "Method not allowed"
                })
            }


quiz_function = QuizFunction(None, None, None)


def handler(request, context):
    # Register quiz information from the makerspace/register console
    # Since this will be hit in prod, it will go ahead and hit our prod
    # dynamodb table
    return quiz_function.handle_quiz_request(
        request, context)
