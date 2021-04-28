# *****
# This lambda contains both update_password and login depending on parameters
# *****

import json
import boto3
from boto3.dynamodb.conditions import Key

# Cognito Client
client = boto3.client('cognito-idp')
clientID = "20nnrq12vp19a99c58g2r0b0og"

statusCode = 200

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Get Table Objects
Users = dynamodb.Table('Users')


def login(email, password):
    global statusCode
    try:
        auth_response = client.initiate_auth(AuthFlow='USER_PASSWORD_AUTH', ClientId=clientID,
                                             AuthParameters={
                                                 'USERNAME': email,
                                                 'PASSWORD': password
                                             })
        print(auth_response)
        statusCode = 200
        return {
            'auth_token': auth_response['AuthenticationResult']['AccessToken']
        }

    except client.exceptions.NotAuthorizedException as e:
        statusCode = 401
        return {
            'Message': "Credentials are incorrect."
        }
    except client.exceptions.UserNotFoundException as e:
        statusCode = 408
        return {
            'Message': "User does not exist."
        }

    except Exception as e:
        # Return exception with response
        statusCode = 403
        return {

            'Message': str(e)

        }


def change_password(old, new, auth_token):
    # update password
    try:
        client.change_password(PreviousPassword=old, ProposedPassword=new, AccessToken=auth_token)
        statusCode = 200
        return {

            'Message': 'The password has been successfully updated. '

        }
    except Exception as e:
        # Return exception with response
        statusCode = 405
        return {

            'Message': str(e)

        }


def loginHandler(event, context):
    data = json.loads(event["body"])
    try:
        result = change_password(data["password"], data["new_password"], data["auth_token"])
        print(result)

        # Send Response
        return {
            'statusCode': 406,
            'headers': {
                'Content-Type': 'text/plain',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps(str(result))
        }

    except:
        # Otherwise login if a new password is not specified
        try:
            result = login(data['email'], data['password'])

            users = Users.scan()
            for user in users["Items"]:
                if user["email"] == data['email']:
                    result["user"] = user
                    break
            #    pass

            # result["user"] = final_user

            # print(result)

            # Send Response
            return {
                'statusCode': statusCode,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },
                'body': json.dumps(result)
            }

        except Exception as e:
            return {
                'statusCode': 407,
                'headers': {
                    'Content-Type': 'text/plain',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },
                'body': json.dumps({'Message': str(e)})
            }




