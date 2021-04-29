import json
from random import randint
import boto3
import os
from base64 import b64encode
import time

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Get Table Objects
Users = dynamodb.Table('Users')


def GenerateUserTokenHandler(event, context):
    try:
        # generating unique visit id
        user_token = b64encode(os.urandom(5)).decode('utf-8')

        # TODO
        # Add user token into some table
        # Record and store time into table as well
        insertToken = dynamodb.Table('userVerificationToken')
        tokenEpochTime = int(time.time())

        input = {'generatedToken': user_token,
                 'tokenTime': tokenEpochTime
                 }

        response = insertToken.put_item(Item=input)

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/plain',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps({'user_token': str(user_token)})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'text/plain',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'message': json.dumps(str(e))
        }

