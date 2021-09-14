import json
import boto3
from boto3.dynamodb.conditions import Key

# poolID = "us-east-1_l5xLuC13j"
db = boto3.resource('dynamodb')
db_client = boto3.client('dynamodb')
client = boto3.client('cognito-idp')
table = db.Table('MakerspaceUser')

# get user role given id


def getUserRole(id):

    # Get user by id
    response = table.query(
        KeyConditionExpression=Key('PK').eq(str(id))
    )

    return(response['Items'][0]['AccessLevel'])


def getUserPK(username):

    query = "SELECT PK FROM MakerspaceUser WHERE Email = '" + username + "'"
    r = db_client.execute_statement(Statement=query)
    return(r['Items'][0]['PK']['S'])


def UpdatePermissionsHandler(event, context):

    #Read in data
    try:
        token = event['token']
        username = event['username']
        new_perm = event['new_perm']
    except BaseException:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'Message': 'Error loading data. '
            })
        }

    # Validate that the user is a manager
    role = getUserRole(token)
    if(role != "manager"):
        return {
            'code': 401,
            'message': 'Insufficient Permissions. '
        }

    try:
        # Get the primary key of the user based on their email
        user_PK = getUserPK(username)

        r = table.update_item(
            Key={
                'PK': user_PK, 'SK': 'Profile'
            },
            UpdateExpression='SET AccessLevel = :newAccessLevel',
            ExpressionAttributeValues={
                ':newAccessLevel': new_perm
            }
        )
    except BaseException:
        return {
            'statusCode': 402,
            'body': json.dumps({
                'Message': 'Error updating permissions. '
            })
        }

    return {
        'code': 200,
        'message': 'Permissions Updated. '
    }
