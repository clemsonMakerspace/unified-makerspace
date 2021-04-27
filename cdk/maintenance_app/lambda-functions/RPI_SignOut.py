import json
import boto3
from boto3.dynamodb.conditions import Key
from random import randint
import time

##
# This function is used for the SignOut process of the Raspberry Pi
# First it will take the hardware ID and cross reference the Visitors DynamoDB table to see if user exists
# If they exist, it will find the most recent signon for the visitor based on the VisitTable
# Will then add logout time to the Visittable
# Any else branches will return with an error code
#
##

db = boto3.resource('dynamodb')
db_client = boto3.client('dynamodb')
visitorTable = db.Table('Visitors')
visitTable = db.Table('Visits')

def RPI_SignOut_Handler(event, context):
    try:
        #getting card id from post command
        data = json.loads(event["body"])
        new_cardID = data['HardwareID']

    except Exception as e:
        print(e)
        return {
                'statusCode': 401,
                'body': json.dumps({
                    'Message' : 'Error loading data. '
                })
        }

    try:
        # check if ID is in MakerspaceUser
        response = visitorTable.query(
            KeyConditionExpression = Key('hardware_id').eq(str(new_cardID))
        )['Items'][0]

    except Exception as e:
        print(e)
        return {
            'statusCode': 402,
            'body': json.dumps({
            'Message' : 'User does not exist! '
            })
        }

    try:
        # check if user is in login table
        visit_response = visitTable.query(
            KeyConditionExpression = Key('visitor_id').eq(str(response["visitor_id"]))
        )['Items'][-1]


    except Exception as e:
        print(e)
        return {
            'statusCode': 403,
            'body': json.dumps({
            'Message' : 'User never signed in! '
            })
        }

    try:
        logoutTime = str(int(time.time()))

        r = visitTable.update_item(
            Key={
                'visitor_id': str(response["visitor_id"]),
                'sign_in_time': visit_response['sign_in_time']
            },
            UpdateExpression='set sign_out_time =:sign_out_time',
            ExpressionAttributeValues={
                ':sign_out_time':logoutTime
            }
        )

    except Exception as e:
        print(e)
        return {
            'statusCode': 404,
            'body': json.dumps({
            'Message' : 'Error in updating table with logout time' + str(e)
            })
        }

    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }
