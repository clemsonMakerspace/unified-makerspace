import boto3
import os

HEADERS = {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS, GET'
        }

def lambda_handler(event, context):
    # Set up the QuickSight client
    quicksight_client = boto3.client('quicksight')

    # Retrieve the AWS Account ID and Dashboard ID from environment variables
    aws_account_id = os.environ.get('AWS_ACCOUNT_ID')
    dashboard_id = os.environ.get('DASHBOARD_ID')

    # Retrieve the User ARN from environment variables
    user_arn = os.environ.get('QUICKSIGHT_USER_ARN') 

    try:
        # Attempt to get the QuickSight dashboard embed URL with session context
        response = quicksight_client.get_dashboard_embed_url(
            AwsAccountId=aws_account_id,
            DashboardId=dashboard_id,
            IdentityType='QUICKSIGHT',
            SessionLifetimeInMinutes=15,
            UndoRedoDisabled=False,
            ResetDisabled=False,
            StatePersistenceEnabled=True,
            UserArn=user_arn  
        )
        
        # If the call is successful, return a success message with the embed URL
        return {
            'headers': HEADERS,
            'statusCode': 200,
            'body': response['EmbedUrl']  # Sending back the actual embed URL
        }

    except quicksight_client.exceptions.QuickSightUserNotFoundException:
        # Handle the case where the QuickSight user is not found
        return {
            'headers': HEADERS,
            'statusCode': 404,
            'body': 'QuickSight user not found.'
        }
    except Exception as e:
        # Handle any other exceptions that might occur
        return {
            'headers': HEADERS,
            'statusCode': 500,
            'body': f'An error occurred: {str(e)}'
        }
