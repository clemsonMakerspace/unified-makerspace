import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
dynamodb_client = boto3.client('dynamodb')

# get student info given student id
def getStudentInfo(id):

    # User Info Table
    table = dynamodb.Table('UserLoginInfo')

    # Get user by id
    response = table.query(
        KeyConditionExpression = Key('StudentID').eq(id)
    )

    # Might need to change this lineW
    return response

def getStudentInfoHandler(event, context):

    params = event['queryStringParameters']

    reqParams = ['StudentID']

    if (params is None):
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': json.dumps( {
                'Message': 'Failed to provide query string parameters'
            })
        }

    for param in reqParams:
        if (param not in params):
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'text/plain'
                },
                'body': json.dumps({
                    'Message': 'Failed to provide parameter: ' + param
                })
            }

    try:
        # Call function
        result = getStudentInfo(params)
        # Send Response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': json.dumps(result)
        }
    except Exception as e:
        # Return exception with response
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': json.dumps({
                'Message': str(e)
            })
        }




