import json
import boto3

# Cognito Client
client = boto3.client('cognito-idp')
clientID = "20nnrq12vp19a99c58g2r0b0og"
poolID = "us-east-1_l5xLuC13j"

def ResetPasswordHandler(event, context):
    # TODO implement
    try: 
        data = json.loads(event["body"])
        username = data['email']
        
        client.admin_reset_user_password({
            UserPoolId=poolID,
            Username=username
        })
    except Exception as e:
        # Return exception with response
        return {
            'statusCode': 500,
            'body': json.dumps({
                'Message': str(e)
            })
        }

