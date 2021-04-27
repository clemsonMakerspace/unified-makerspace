import json
import boto3
from boto3.dynamodb.conditions import Key
from random import randint
import time
import os
import base64


##
# This function is used for the SignIn process of the Raspberry Pi
# First it will take the hardware ID and cross reference the Visitors DynamoDB table to see if user exists
# If they exist, it will pull the data for the user from the MakerspaceUser DynamoDB table and add it to the Visit Table
# Any else branches will return with an error code
#
##

db = boto3.resource('dynamodb')
db_client = boto3.client('dynamodb')
visitorsTable = db.Table('Visitors')
visitTable = db.Table('Visits')

def RPI_SignIn_Handler(event, context):

    try:
        data = json.loads(event["body"])
        new_cardID = data['HardwareID']
        location = data['LoginLocation']

    except Exception as e:
        print(e)
        return {
                'statusCode': 401,
                'body': json.dumps({
                    'Message' : 'Error loading data. '
                })
        }

    try:
        # check if ID is in Visitors
        response = visitorsTable.query(
            KeyConditionExpression = Key('hardware_id').eq(str(new_cardID))
        )['Items'][0]

        try:
            print("item in visitors table")

            #querying to see how many times the user has been in the space
            num_visits_response = visitTable.query(
                KeyConditionExpression = Key('visitor_id').eq(str(response['visitor_id']))
            )['Items']

            if len(num_visits_response) == 0:
                first_visit = True
            else:
                first_visit = False

            time_in = int(time.time())

            #generating unique visit id
            visit_id = base64.b64encode(os.urandom(16)).decode('utf-8')
            print("the visit id is " + visit_id)

            #get items from visitors table then add new entry to visits table
            #items needed in visits table is visitor_id, date_visited, first_visit, login_location, sign_in_time, sign_out_time, visit_id
            new_login = {"visitor_id": str(response["visitor_id"]), "date_visited": time_in, "first_visit": first_visit, "login_location": str(location), "sign_in_time": time_in, "visit_id": str(visit_id)}

            visitTable.put_item(Item=new_login)

            print("User successfully Added to Login Table")

        except Exception as e:
            print(e)
            message_text = 'User not successfully added to visit table' + 'trying to put visit info as ' + str(new_login)
            return {
            'statusCode': 403,
            'body': json.dumps({
            'Message' : message_text
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
