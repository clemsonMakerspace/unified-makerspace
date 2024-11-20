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
bucket_name = os.environ['BUCKET_NAME']

#! WIP
def lambda_handler(event, context):
    try:
        # Check if the bucket exists
        try:
            s3_client.head_bucket(Bucket=bucket_name)
            logger.info(f"Bucket {bucket_name} exists.")
        except ClientError as e:
            # Handle the error if the bucket does not exist
            logger.error(f"Bucket {bucket_name} does not exist: {str(e)}")
            raise Exception(f"Bucket {bucket_name} does not exist. Aborting the process.")
        
        # List objects in the S3 bucket
        logger.info(f"Listing objects in bucket: {bucket_name}")
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        
        # Check if the bucket contains objects
        if 'Contents' not in response:
            logger.info("No files found in the bucket.")
            return {
                'statusCode': 200,
                'body': 'No files found in the S3 bucket.'
            }
        
        # Trigger Glue job for each CSV file in the S3 bucket
        for item in response['Contents']:
            file_key = item['Key']
            
            # Trigger the Glue job for the file
            logger.info(f"Triggering Glue job for file: {file_key}")
            glue_client.start_job_run(
                JobName='beta-S3Pull-CSVParse-DDBStore',  # Glue job name
                Arguments={
                    '--s3_input': f"s3://{bucket_name}/{file_key}"
                }
            )
        
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
