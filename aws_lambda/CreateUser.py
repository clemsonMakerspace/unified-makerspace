# FROM MAKERSPACE MANAGER LAMBDA APPLICATION

import decimal
import time
import boto3
import json
import uuid
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from boto3.dynamodb.conditions import Key
from api.models import User
from base64 import b64encode
import os


clientID = "20nnrq12vp19a99c58g2r0b0og"
poolID = "us-east-1_l5xLuC13j"

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Get Table Objects
Users = dynamodb.Table('Users')
User_tokens = dynamodb.Table('userVerificationToken')

# Cognito Client
client = boto3.client('cognito-idp')

def CreateUser(data):
    new_user = json.loads(data["body"])
    
    print(new_user)
    user_token = new_user["user_token"]
    email = new_user["email"]
    password = new_user["password"]
    first_name = new_user["first_name"]
    last_name = new_user["last_name"]
    
    
    # Check if user_token is in the tokens table
    # If it is, check how old
    # Return error if either does not check
    try:
        currentTime = int(time.time()) - 18000
        response = User_tokens.query(
            KeyConditionExpression = Key('generatedToken').eq(str(user_token))
        )
        
        generatedTime = int(response['Items'][0]['tokenTime'])
        
        #check if they are 5 min apart
        if (abs(currentTime-generatedTime) > 300):
            return {
                'code': 406,
                'message' : json.dumps("Token is expired")
            }
    except:
        return {
                'code': 405,
                'message' : json.dumps("Could not validate token")
        }
    custom_attributes = [
        {'Name': 'email', 'Value': email},
        {'Name': 'custom:firstname', 'Value': first_name},
        {'Name': 'custom:lastname', 'Value': last_name}
    ]

    try:
        #Create new user in cognito pool
        response = client.sign_up(ClientId=clientID, Username=email, Password=password, UserAttributes=custom_attributes)

    except client.exceptions.UsernameExistsException as e:
        #Return error if email is already in use
        return {
                'code': 400,
                'message' : 'This email is already being used. '
        }
    except Exception as e:
        return {
                'code': 402,
                'message' : json.dumps(str(e))
        }

    # Generate user_id and store into database
    # Store user into the database
    userId = b64encode(os.urandom(6)).decode('utf-8')
    user_obj = User(userId, new_user["first_name"], new_user["last_name"], [], [])
    user_data = {'user_id':userId, 'assigned_tasks':[], 'first_name':first_name, 'last_name':last_name, 'user_permissions':[], 'email':email}
    Users.put_item(Item=user_data)

    # Get token for new user
    try:
        auth_response = client.initiate_auth(AuthFlow='USER_PASSWORD_AUTH', ClientId=clientID,
                                             AuthParameters = {
                                                 'USERNAME': email,
                                                 'PASSWORD': password
                                         })
    except Exception as e:
        return {
                'code': 403,
                'message' : json.dumps(str(e))
        }

    print(auth_response)

    return {
            'statusCode': 200,
            'user':json.dumps(user_obj.__dict__),
            'auth_token': auth_response['AuthenticationResult']['AccessToken']
        }


def CreateUserHandler(event, context):
    # Return client error if no string params
    if (event is None):
        return {
            'statusCode': 400,
            'body': json.dumps({
                'Message': 'Failed to provide query string parameters.'
            })
        }

    try:
        # Call function
        result = CreateUser(event)
        print(result)

        # Send Response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/plain',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'

            },
            'body': json.dumps(result)
        }
    except Exception as e:
        # Return exception with response
        return {
            'statusCode': 500,
            'body': json.dumps({
                'Message': str(e)
            })
        }