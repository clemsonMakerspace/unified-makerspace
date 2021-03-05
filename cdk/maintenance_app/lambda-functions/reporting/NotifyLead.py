import boto3
import os
from bs4 import BeautifulSoup
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime, timedelta

# Get the service resources
dynamodb = boto3.resource('dynamodb')
ses_client = boto3.client('ses')
s3_client = boto3.client('s3')

#Get Table Objects
Child_Table = dynamodb.Table('Child_Tasks')

#GetBucketArn
bucketName = os.environ['bucketName']

#Check Email Verification for SES
def VerifyEmail(email):

    #Get All Email Identities
    identities = ses_client.list_identities(
        IdentityType='EmailAddress',
        MaxItems=1000,
        NextToken='',
    )['Identities']

    #Check if email exists in identities
    if email in identities:
        return True

    #Verify Email if not
    ses_client.verify_email_identity(
        EmailAddress=email
    )

    #Return false bc identity is not verified
    return False

#Get's Sender Email from S3 bucket
def GetSender():

    #Get object from s3 object
    senderObj = s3_client.get_object(
        Bucket=bucketName,
        Key='sender'
    )

    #Read Email from object
    senderEmail = senderObj['Body'].read()

    return senderEmail.decode()

#Get's Recipient's Email from S3 bucket
def GetRecipient():

    #Get object from s3 object
    recipientObj = s3_client.get_object(
        Bucket=bucketName,
        Key='recipient'
    )

    #Read Email from object
    recipientEmail = recipientObj['Body'].read()

    return recipientEmail.decode()

#Retrieves Incomplete Task From Dynamo Db
def GetIncompleteTasks():

    #Today's Key
    today = datetime.now().strftime('%Y%m%d')

    #Get Today's Incomplete Child Tasks
    children = Child_Table.query(
        KeyConditionExpression=Key('Due_Date').eq(today),
        FilterExpression=Attr('Completed').eq(0)
            &Attr('Active').eq(1)
    )['Items']

    return children

#Returns formatted Time String
def GetTimeStr(time):

    #Convert Str to int
    time = int(time)

    #Calculate hour
    hour = (time/100) % 12
    hour = 12 if (hour == 0) else hour

    #Calculate minute
    minute = time % 100

    #Calculate period
    period = "AM" if hour >= 12 else "PM"

    #Return formatted time string (e.g. 10:15 PM)
    return str(int(hour)) + ":" + str(minute).zfill(2) + ' ' + period

#Returns List Indexes For Tasks
def GetTasksHtml(tasks):

    tasksList = ''

    for t in tasks:
        tasksList += "<li>"
        tasksList += (t['Machine_Name'] + ': ')
        tasksList += (t['Task_Name'] + ' by ')
        tasksList += (GetTimeStr(t['Due_Time']))
        tasksList += "</li>"

    return tasksList

#Returns Html for Notification Email
def GetEmailHtml(tasks):

    tasksHtml = GetTasksHtml(tasks)
    today = datetime.now().strftime("%m-%d-%Y")

    emailHtml = """
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            li {
                font-size: 18px;
                line-height: 1.5;
            }
        </style>
        </head>

        <body>
            <h2>Incomplete Tasks For %s:</h2>
            <ul>
                %s
            </ul>
        </body>
        </html>
    """ % (today, tasksHtml)

    return emailHtml

#Send Email Notification for Incomplete Tasks
def SendNotificationEmail(tasks):

    today = datetime.now().strftime("%m-%d-%Y")

    #Email Parameters
    sender = GetSender()
    recipient = GetRecipient()
    charset = "UTF-8"
    body_html = GetEmailHtml(tasks)
    body_text = BeautifulSoup(body_html, 'html.parser').get_text()
    subject = "CU Makerspace - Late Tasks for " + today
    
    #Check Email Verification
    if(not VerifyEmail(sender)):
        return "Sender " + sender + " not verified."

    #Check Email Verification
    if(not VerifyEmail(recipient)):
        return "Recipient " + recipient + " not verified."

    #Send Notification Emails
    ses_client.send_email(
        Source= sender,
        Destination={
            'ToAddresses': [recipient]
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': charset,
                    'Data': body_html,
                },
                'Text': {
                    'Charset': charset,
                    'Data': body_text,
                },
            },
            'Subject': {
                'Charset': charset,
                'Data': subject,
            },
        }
    )
        
def NotifyLeadHandler(event, context):

    #Get Today's Incomplete Tasks
    tasks = GetIncompleteTasks()

    #Send Email With Incomplete Tasks
    response = SendNotificationEmail(tasks)

    #Send Response
    return response