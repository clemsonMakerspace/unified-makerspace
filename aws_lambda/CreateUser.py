import json
import boto3

clientID = "20nnrq12vp19a99c58g2r0b0og" 

def CreateUserHandler(event, context):
    
    username = event['username']
    password = event["password"]
    role = event['role']
    email = event['email']
    first_name = event["first"]
    last_name = event["last"]
    
    client = boto3.client('cognito-idp')
    custom_attributes = [
        {'Name' : 'email', 'Value': email},
        {'Name' : 'custom:firstname', 'Value': first_name}, 
        {'Name' : 'custom:lastname', 'Value': last_name}, 
        {'Name' : 'custom:role', 'Value': role}
        ]

    try:
        response = client.sign_up(ClientId=clientID, Username=username, Password=password, UserAttributes=custom_attributes)
    except client.exceptions.UsernameExistsException as e:
        return {
                'statusCode': 400,
                'body': json.dumps('This email is already being used. ')
        }
        
        
    if response['UserConfirmed'] == True:
        return {
                'statusCode': 200,
                'body': json.dumps('The user has been successfully created. ')
        }
        