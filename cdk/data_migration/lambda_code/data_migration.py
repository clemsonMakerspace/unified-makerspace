import boto3
import logging
import os
from botocore.exceptions import ClientError

# Initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# AWS clients
s3_client = boto3.client('s3')
glue_client = boto3.client('glue')

# Environment variables
bucket_name = os.environ['BUCKET_NAME']
glue_job_name = os.environ['GLUE_JOB_NAME']

def lambda_handler(event, context):
    """
    Lambda handler to scan Beta S3 bucket for files and trigger Glue job.
    """
    try:
        # List objects in the Beta S3 bucket
        response = s3_client.list_objects_v2(Bucket=bucket_name)

        if 'Contents' not in response or not response['Contents']:
            logger.info("No files found in the bucket.")
            return {"statusCode": 200, "body": "No files found in the bucket."}

        # Trigger Glue job for each file in the bucket
        for item in response['Contents']:
            file_key = item['Key']
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
                logger.error(f"Failed to trigger Glue job for file {file_key}: {e}")

        return {"statusCode": 200, "body": "Glue job triggered for all files in the bucket."}

    except Exception as e:
        logger.error(f"Error processing files: {e}")
        return {"statusCode": 500, "body": f"Error: {e}"}
