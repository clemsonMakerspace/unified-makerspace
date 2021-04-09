import json
import boto3
from boto3.dynamodb.conditions import Key
from random import randint
import time

##
# This function is used for the SignOut process of the Raspberry Pi
# First it will take the hardware ID and cross reference the MakerspaceUser DynamoDB table to see if user exists
# If they exist, it will find the most recent signon for the user based on the LoginTable
# Will then add logout time to the table
# Any else branches will return with an error code
#
##
db = boto3.resource('dynamodb')
db_client = boto3.client('dynamodb')
userTable = db.Table('MakerspaceUser')
loginTable = db.Table('UserLoginInfo')

def SignOutHandler(event, context):
    try:
        #getting card id from post command
        new_cardID = event['HardwareID']
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
        response = userTable.query(
            KeyConditionExpression = Key('HardwareID').eq(str(new_cardID))
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
        login_response = loginTable.query(
            KeyConditionExpression = Key('HardwareID').eq(str(new_cardID))
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

        r = loginTable.update_item(
            Key={
                'HardwareID': new_cardID,
                'LoginTime': login_response['LoginTime']
            },
            UpdateExpression='set LogoutTime =:logoutTime',
            ExpressionAttributeValues={
                ':logoutTime':logoutTime
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
