import json
import boto3
from boto3.dynamodb.conditions import Key
from random import randint
import time


##
# This function is used for the SignOn process of the Raspberry Pi
# First it will take the hardware ID and cross reference the MakerspaceUser DynamoDB table to see if user exists
# If they exist, it will pull the data for the user from the MakerspaceUser DynamoDB table and add it to the UserLogin Table
# Any else branches will return with an error code
#
##
db = boto3.resource('dynamodb')
db_client = boto3.client('dynamodb')
userTable = db.Table('MakerspaceUser')
loginTable = db.Table('UserLoginInfo')

def SignInHandler(event, context):
    try:
        new_cardID = event['HardwareID']
        location = event['LoginLocation']

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

        try:
            print("item in makerspace user")
            #get times from table then add new entry to login table
            #items needed in login table is HardwareID, LoginTime, DegreeType, FirstName, LastName, LoginLocation, Major
            new_login = {'HardwareID': new_cardID, 'LoginTime': int(time.time()), 'DegreeType': response['DegreeType'], 'FirstName': response['FirstName'], 'LastName': response['LastName'], 'LoginLocation': str(location), 'Major': response['Major'], 'VisitID': str(randint(1000000000, 9999999999))}
            loginTable.put_item(Item=new_login)
            print("User successfully Added to Login Table")
        except Exception as e:
            print(e)
            return {
            'statusCode': 403,
            'body': json.dumps({
            'Message' : 'User Not Successfully Added to Login Table '
            })
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 402,
            'body': json.dumps({
            'Message' : 'User does not exist! '
            })
        }

    return {
        'statusCode': 200,
        'body': json.dumps('Success')
        }
