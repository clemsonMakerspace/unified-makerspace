import json
import boto3
from boto3.dynamodb.conditions import Key

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Get Table Objects
table = dynamodb.Table('Users')


def UpdateUserHandler(event, context):
    try:
        data = json.loads(event['body'])
        user_id = data['user_id']
    except:
        # Send Error
        return {
            'statusCode': 200,
            'body': json.dumps("Error reading data")
        }

    try:
        # Get email of user (should not be changed)
        response = table.query(
            KeyConditionExpression=Key('user_id').eq(str(user_id))
        )
        email = response['Items'][0]['email']

        r = table.update_item(
            Key={
                'user_id': user_id
            },
            UpdateExpression='SET assigned_tasks = :new_tasks, first_name = :first, last_name = :last, user_permissions = :perm, email=:sameEmail',
            ExpressionAttributeValues={
                ':new_tasks': data['assigned_tasks'],
                ':first': data['first_name'],
                ':last': data['last_name'],
                ':perm': data['permissions'],
                ':sameEmail': email
            }
        )

        # Send Response
        return {
            'statusCode': 200,
            'body': json.dumps(r)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'Message': str(e)
            })
        }
