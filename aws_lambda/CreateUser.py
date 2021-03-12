import json
import boto3

clientID = "20nnrq12vp19a99c58g2r0b0og" 

def CreateUserHandler(event, context):
    try:
        username = event['username']
        password = event["password"]
        cardID = event['cardID']
        email = event['email']
        first_name = event["first"]
        last_name = event["last"]
    except:
        return {
                'statusCode': 401,
                'body': json.dumps({
                    'Message' : 'Error loading data. '
                 })
        }
        
    #AWS resources
    client = boto3.client('cognito-idp')
    
    db = boto3.resource('dynamodb')
    table = db.Table('MakerspaceUser')
    
    custom_attributes = [
        {'Name' : 'email', 'Value': email},
        {'Name' : 'custom:firstname', 'Value': first_name}, 
        {'Name' : 'custom:lastname', 'Value': last_name}
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
    
    #Get token for new user
    auth_token = response['UserSub']
   
    #Store user data in databse
    new_user = {'PK':auth_token, 'SK':"Profile", 'AccessLevel':"student", 'Email':email, 'First_Name':first_name, 'Last_Name':last_name, 'cardID':cardID}
    table.put_item(Item=new_user)
    
    return {
            'code': 200,
            'message': 'The user has been successfully created. ',
             'auth_token':auth_token
    }
        