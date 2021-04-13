import json
import boto3
from boto3.dynamodb.conditions import Key

poolID = "us-east-1_l5xLuC13j"
db = boto3.resource('dynamodb')
db_client = boto3.client('dynamodb')
client = boto3.client('cognito-idp')
table = db.Table('MakerspaceUser')
 
# get user role given id
def getUserRole(id):

    # Get user by id
    response = table.query(
        KeyConditionExpression = Key('PK').eq(str(id))
    )
    
    return(response['Items'][0]['AccessLevel'])
    
def getUserPK(username):
    
    query = "SELECT PK FROM MakerspaceUser WHERE Email = '" + username + "'"
    r = db_client.execute_statement(Statement=query)
    return(r['Items'][0]['PK']['S'])
    
def DeleteUserHandler(event, context):
    try:
        username = event['username']
        auth_token = event['auth_token']
    except:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'Message' : 'Error loading data. '
             })
        }
    
    role = getUserRole(auth_token)
    if(role != "manag"):
        return {
            'code': 401,
            'message' : 'Insufficient Permissions. '
        }

    key = getUserPK(username)
    
    try:
        #Remove user from cognito
        response = client.admin_delete_user(UserPoolId=poolID, Username=username)
        #remove user from database
        table.delete_item(
                Key = {
                    'PK' : key,
                    'SK' : "Profile"
                }
            )
    except Exception as e:
        return {
            'code': 401,
            'message': "Error removing user"
        }
    
    return {
            'code': 200,
            'message' : 'User Deleted. '
        }
