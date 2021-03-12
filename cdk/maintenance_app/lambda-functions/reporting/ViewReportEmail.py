import boto3
import json
import os

# Get the service resources
s3_client = boto3.client('s3')

#GetBucketArn
bucketName = os.environ['bucketName']

def ViewReportEmail(params):

    #Get Parameters
    role = params['Role']

    #Get object from s3 object
    emailObj = s3_client.get_object(
        Bucket=bucketName,
        Key=role
    )

    #Read Email from object
    email = emailObj['Body'].read()

    return email.decode()

def ViewReportEmailHandler(event, context):

    reqParams = ['Role']

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
        result = ViewReportEmail(paramVals)

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