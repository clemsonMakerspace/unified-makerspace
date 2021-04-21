# *****
# This lambda contains both change_password and login depending on parameters
# *****

import json
import boto3
import json
from boto3.dynamodb.conditions import Key

# Cognito Client
client = boto3.client('cognito-idp')
clientID = "20nnrq12vp19a99c58g2r0b0og"

def login(email, password):
    try:
        auth_response = client.initiate_auth(AuthFlow='USER_PASSWORD_AUTH', ClientId=clientID,
                                     AuthParameters = {
                                         'USERNAME': email,
                                         'PASSWORD': password
                                 }) 
        print(auth_response)
        return {
            'statusCode': 200,
            'auth_token': auth_response['AuthenticationResult']['AccessToken']
        }
    except Exception as e:
        # Return exception with response
        return {
            'statusCode': 403,
            'message': e
        }
        
        
        
def change_password(old, new, auth_token):
     #update password
    try:
        client.change_password(PreviousPassword=old, ProposedPassword=new, AccessToken=auth_token)
        return {
            'statusCode': 200,
            'message': 'The password has been successfully updated. '
        }
    except Exception as e:
        # Return exception with response
        return {
            'statusCode': 403,
            'message': e
        }
            
def loginHandler(event, context):
  
    
    data = json.loads(event["body"])
    try:
        result = change_password(data["password"], data["new_password"], data["auth_token"])
        print(result)
        
        # Send Response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': json.dumps(str(result))
        }
        
    except:
        #Otherwise login if a new password is not specified
        try:
            result = login(data['email'], data['password'])
            
            print(result)
            
            # Send Response
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'text/plain'
                },
                'body': json.dumps(str(result))
            }
            
        except:
            return {
                'statusCode': 400,
                'body': json.dumps({'Message': 'Error reading data'})
            }
        
            
            

    