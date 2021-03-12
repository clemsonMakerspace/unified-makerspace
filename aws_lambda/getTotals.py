import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
dynamodb_client = boto3.client('dynamodb')

# get student info given student id
def getTotals():

    # User Info Table
    table = dynamodb.Table('MakerspaceUser')

    response = table.scan(
        #Get majors
        FilterExpression = Attr('Major').eq('Computer Science') &
        #Get years
        Attr('Year').eq('2021') &
        #Get colleges
        Attr('College').eq('Clemson')
    )
    #TODO: Add query for other majors,years,colleges

    # Might need to change this line
    return response['Item']

def getTotalsHandler(event, context):

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
        result = getTotals()
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





