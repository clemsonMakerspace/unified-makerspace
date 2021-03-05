import boto3
import json
import os

# Get the service resources
ses_client = boto3.client('ses')
s3_client = boto3.client('s3')

#GetBucketArn
bucketName = os.environ['bucketName']

def UpdateReportEmail(params):

    #Get Parameters
    role = params['Role']
    email = params['Email']

    #Update S3 bucket object
    s3_client.put_object(
        Body=email.encode(),
        Bucket=bucketName,
        Key=role,
    )

    #Not sure if calling verify on an email more than once
    #will cause an error. May have to list identities and check.

    #Verify Email
    ses_client.verify_email_identity(
        EmailAddress=email
    )

    return "Verification email sent to " + email

def UpdateReportEmailHandler(event, context):

    reqParams = ['Email', 'Role']

    #Get Query Params
    paramVals = event["queryStringParameters"]

    #Return client error if no string params
    if (paramVals is None):
        return{
            'statusCode': 400,
            'headers':{
                'Content-Type': 'text/plain'
            },
            'body': json.dumps({
                'Message' : 'Failed to provide query string parameters.'
            })
        }

    #Check for each parameter we need
    for name in reqParams:
        if (name not in paramVals):
            return {
                'statusCode': 400,
                'headers':{
                    'Content-Type': 'text/plain'
                },
                'body': json.dumps({
                    'Message' : 'Failed to provide parameter: ' + name
                })
            }   

    #Check for Sender or Recipient
    role = paramVals['Role']
    
    if (role != 'sender' and role != 'recipient'):
        return {
            'statusCode': 400,
            'headers':{
                'Content-Type': 'text/plain'
            },
            'body': json.dumps({
                'Message' : "Value of 'Role' must be 'sender' or 'recipient'"
            })
        } 

    try:
        #Call function
        result = UpdateReportEmail(paramVals)

        #Send Response
        return {
            'statusCode': 200,
            'headers':{
                'Content-Type': 'text/plain'
            },
            'body': json.dumps(result)
        }
    except Exception as e:
        #Return exception with response
        return {
            'statusCode': 500,
            'headers':{
                'Content-Type': 'text/plain'
            },
            'body': json.dumps({
                'Message' : str(e)
            }) 
        }