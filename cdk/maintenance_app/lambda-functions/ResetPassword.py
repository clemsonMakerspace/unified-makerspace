import json
import boto3
import os

# Cognito Client
client = boto3.client('cognito-idp')
# clientID = "20nnrq12vp19a99c58g2r0b0og"
clientID = os.environ['user_cognitoClientID']
# poolID = "us-east-1_l5xLuC13j"


def ResetPasswordHandler(event, context):
    try:
        username = event["email"]

        client.forgot_password(ClientId=clientID, Username=username)
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/plain',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'

            },
            'message': json.dumps(str("Reset password email sent."))
        }
    except Exception as e:
        # Return exception with response
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

