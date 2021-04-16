#TODO: If called by maintainer, only retrieve names

import json
import boto3
from boto3.dynamodb.conditions import Key
from api.models import User

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Get Table Objects
Users = dynamodb.Table('Users')
        
def obj_dict(obj):
    return obj.__dict__
        
def GetUsersHandler(event, context):
    try:
        users_string = event['queryStringParameters']['users']
        users_list = users_string.split(',')
    except:
        #If list is not specified, return all users
        all_users = Users.scan()
        users_list = []
        for user in all_users['Items']:
            
            new_user = User(user_id = user['user_id'], first_name = user['first_name'], last_name= user['last_name'], assigned_tasks=user['assigned_tasks'], permissions= user['user_permissions'])
            users_list.append(new_user)
        
        return {
            'statusCode': 200,
            'body': json.dumps(users_list, default=obj_dict)
        }
        
        
    user_objects = []
    
    for user in users_list:
        # Get user by id
        response = Users.query(
            KeyConditionExpression = Key('user_id').eq(str(user))
        )
        row = response['Items'][0]
        
        new_user = User(user_id = row['user_id'], first_name = row['first_name'], last_name= row['last_name'], assigned_tasks=row['assigned_tasks'], permissions= row['user_permissions'])
        
        user_objects.append(new_user)
    
    return {
        'statusCode': 200,
        'body': json.dumps(user_objects, default=obj_dict)
    }