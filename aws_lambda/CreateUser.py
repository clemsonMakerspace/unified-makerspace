# FROM MAKERSPACE MANAGER LAMBDA APPLICATION


import boto3
import json
import uuid
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from boto3.dynamodb.conditions import Key
from api.models import User

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Get Table Objects

# DEPRECATED: TO REMOVE
# Parent_Table = dynamodb.Table('Parent_Tasks')
# Child_Table = dynamodb.Table('Child_Tasks')
# Machine_Table = dynamodb.Table('Machines')

Users = dynamodb.Table('Users')

# Cognito Client
client = boto3.client('cognito-idp')


def CreateUser(data):
    new_user = json.loads(data["body"])

    new_user = User(new_user["first_name"], new_user["last_name"], new_user["email"], new_user["password"],
                    new_user["user_token"])

    # Put new task into the tasks eventbase
    Users.put_item(
        Item=new_user.__dict__
    )

    custom_attributes = [
        {'Name': 'email', 'Value': new_user.email},
        {'Name': 'custom:firstname', 'Value': new_user.first_name},
        {'Name': 'custom:lastname', 'Value': new_user.last_name}
    ]

    try:
        #Create new user in cognito pool
        response = client.sign_up(ClientId=clientID, Username=username, Password=password, UserAttributes=custom_attributes)
    except client.exceptions.UsernameExistsException as e:
        #Return error if email is already in use
        return {
                'code': 400,
                'message' : 'This email is already being used. '
        }
    except Exception as e:
        return {
                'code': 402,
                'message' : e
        }

    # Get token for new user
    auth_token = response['UserSub']

    return {
        'code': 200,
        'message': 'The user has been successfully created. ',
        'auth_token': auth_token
    }


def CreateUserHandler(event, context):

    # Return client error if no string params
    if (event is None):
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': json.dumps({
                'Message': 'Failed to provide query string parameters.'
            })
        }

    try:
        # Call function
        result = CreateUser(event)

        # Send Response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': json.dumps(result)
        }
    except Exception as e:
        # Return exception with response
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': json.dumps({
                'Message': str(e)
            })
        }