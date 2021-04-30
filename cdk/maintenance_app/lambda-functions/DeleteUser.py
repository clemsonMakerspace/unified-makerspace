import json
import boto3
from boto3.dynamodb.conditions import Key
import os

# poolID = "us-east-1_l5xLuC13j"
poolID = os.environ['user_cognitoUserPoolID']

db = boto3.resource('dynamodb')
db_client = boto3.client('dynamodb')
client = boto3.client('cognito-idp')
table = db.Table('Users')


def DeleteUserHandler(event, context):

    try:
        data = json.loads(event["body"])
        user_id = data['user_id']
    except:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'Message': "Error loading data"
            })
        }

    try:
        #Get username of user to delete
        response = table.query(
            KeyConditionExpression = Key('user_id').eq(str(user_id))
        )
        user = response['Items'][0]
    except:
        return {
            'statusCode': 401,
            'body': json.dumps({
                'Message': "Error finding user"
            })
        }

    try:
        #Remove the user from cognito pool
        response = client.admin_delete_user(UserPoolId=poolID, Username=user['email'])
    except Exception as e:
        # Return exception with response
        return {
            'statusCode': 501,
            'body': json.dumps({
                'Message': str(e)
            })
        }

    #Remove user from database
    try:
        table.delete_item(
                Key = {
                    'user_id' : user_id,
                }
                )
    except Exception as e:
        # Return exception with response
        return {
            'statusCode': 501,
            'body': json.dumps({
                'Message': str(e)
            })
        }

    #TODO:
    #Depreciate any tasks assigned to the user

    return {
            'statusCode': 200,
            'body': json.dumps({
                'Message': "User deleted"
            })
        }
