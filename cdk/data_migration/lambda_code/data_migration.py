
import boto3
import logging
import os
from botocore.exceptions import ClientError

# Initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
s3_client = boto3.client('s3')
glue_client = boto3.client('glue')

# S3 bucket name (this will come from the environment variable)
bucket_name = os.environ.get('BUCKET_NAME')

def lambda_handler(event, context):
    """
    Lambda handler function to process S3 files and trigger Glue jobs.
    """
    try:
        # Check if the bucket name is provided
        if not bucket_name:
            logger.error("Environment variable BUCKET_NAME is not set.")
            return {
                'statusCode': 400,
                'body': 'Environment variable BUCKET_NAME is not set.'
            }

        # Check if the bucket exists
        try:
            s3_client.head_bucket(Bucket=bucket_name)
            logger.info(f"Bucket {bucket_name} exists.")
        except ClientError as e:
            # Handle the error if the bucket does not exist
            logger.error(f"Bucket {bucket_name} does not exist: {str(e)}")
            return {
                'statusCode': 404,
                'body': f"Bucket {bucket_name} does not exist. Aborting the process."
            }
        
        # List objects in the S3 bucket
        logger.info(f"Listing objects in bucket: {bucket_name}")
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        
        # Check if the bucket contains objects
        if 'Contents' not in response or not response['Contents']:
            logger.info("No files found in the bucket.")
            return {
                'statusCode': 200,
                'body': 'No files found in the S3 bucket.'
            }
        
        # Trigger Glue job for each CSV file in the S3 bucket
        glue_job_name = 'beta-S3Pull-CSVParse-DDBStore'  # Glue job name
        logger.info(f"Glue Job Name: {glue_job_name}")

        for item in response['Contents']:
            file_key = item['Key']
            
            # Trigger the Glue job for the file
            logger.info(f"Triggering Glue job for file: {file_key}")
            try:
                glue_client.start_job_run(
                    JobName=glue_job_name,
                    Arguments={
                        '--s3_input': f"s3://{bucket_name}/{file_key}"
                    }
                )
                logger.info(f"Successfully triggered Glue job for file: {file_key}")
            except ClientError as e:
                logger.error(f"Failed to trigger Glue job for file {file_key}: {str(e)}")
        
        return {
            'statusCode': 200,
            'body': 'Glue job triggered for each file in the bucket.'
        }
    
    except Exception as e:
        logger.error(f"Error processing files: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }
