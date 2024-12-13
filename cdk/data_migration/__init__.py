from aws_cdk import (
    Stack,
    Environment,
    aws_lambda as lambda_,
    aws_iam as iam,
    aws_glue as glue,
    aws_s3 as s3,
    aws_s3_deployment as s3_deployment,
    custom_resources as cr,
    CfnOutput,
    RemovalPolicy
)
from constructs import Construct
import json

from ..accounts_config import accounts


class DataMigrationStack(Stack):
    """
    The DataMigrationStack is responsible for setting up the infrastructure required to 
    migrate data from a Beta environment's S3 bucket into a production environment, 
    leveraging AWS Glue for ETL (Extract, Transform, Load) operations.

    This stack performs the following tasks:
    - Defines a temporary S3 bucket to store intermediate Glue job data.
    - Sets up an AWS Glue Job with a dedicated IAM role for permissions.
    - Deploys a Lambda function to trigger the Glue job.
    - Applies a cross-account bucket policy to allow access to the Beta S3 bucket.
    - Deploys the Glue script to the temporary S3 bucket.

    Parameters:
    - scope (Construct): The scope in which this construct is defined.
    - id (str): The unique identifier for this stack.
    - env (Environment): The AWS environment in which the stack is deployed, including the account and region.

    Key Resources:
    - S3 Buckets:
        - Temporary bucket for Glue job storage.
        - Beta S3 bucket for source data (cross-account access).
    - IAM Roles:
        - Glue Job Role with access to S3 and DynamoDB.
    - AWS Glue Job:
        - Processes data from the Beta S3 bucket and stores the results in DynamoDB.
    - Lambda Function:
        - Triggers the Glue job programmatically.
    - Cross-Account Bucket Policy:
        - Allows the Glue Job Role to access the Beta S3 bucket.

    Outputs:
    - GlueJobName: The name of the AWS Glue job created.
    - TriggerLambdaARN: The ARN of the Lambda function that triggers the Glue job.
    - TempBucketName: The name of the temporary S3 bucket for Glue job storage.

    Notes:
    - Ensure the `accounts_config` module is properly configured with account and region details for the Beta and Prod environments.
    - The Glue script should be located in the `data_migration` directory under the project root.

    Documentation Links:
        - aws_glue.CfnJob:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_glue/CfnJob.html
        - aws_s3.Bucket:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_s3/Bucket.html
        - aws_s3_deployment.BucketDeployment:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_s3_deployment/BucketDeployment.html
        - aws_iam.Role:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_iam/Role.html
        - aws_lambda.Function:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html
        - aws_s3.BucketPolicy:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_s3/BucketPolicy.html
        - custom_resources.AwsCustomResource:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.custom_resources/AwsCustomResource.html
    """
    def __init__(self, scope: Construct, id: str, *, env: Environment) -> None:
        super().__init__(scope, id, env=env)

        # Get Beta and Prod environment information
        beta_account_id = accounts["Beta"]["account"]
        beta_region = accounts["Beta"]["region"]

        prod_account_id = accounts["Prod"]["account"]
        prod_region = accounts["Prod"]["region"]

        # Define the Beta S3 bucket for CSV files
        beta_bucket_name = "csvs-for-glue-job"

        # Create a dedicated S3 bucket for Glue temporary data
        temp_bucket = s3.Bucket(self, "GlueTempBucket",
            removal_policy=RemovalPolicy.DESTROY,  # Destroy on stack deletion
            auto_delete_objects=True,  # Allow deleting objects when bucket is destroyed
        )

        # Define the IAM role for the Glue job
        glue_role = iam.Role(self, "GlueJobRole",
            assumed_by=iam.ServicePrincipal("glue.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSGlueServiceRole"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"),
            ]
        )

        # Add explicit permissions for Glue role to access the Beta bucket
        glue_role.add_to_policy(
            iam.PolicyStatement(
                actions=["s3:GetObject", "s3:ListBucket"],
                resources=[
                    f"arn:aws:s3:::{beta_bucket_name}",
                    f"arn:aws:s3:::{beta_bucket_name}/*"
                ]
            )
        )

        # Upload the Glue script to the temporary bucket
        glue_script_path = f"s3://{temp_bucket.bucket_name}/scripts/data_migration.py"
        s3_deployment.BucketDeployment(self, "DeployGlueScript",
            sources=[s3_deployment.Source.asset("data_migration")],
            destination_bucket=temp_bucket,
            destination_key_prefix="scripts"
        )

        # Create the Glue job
        glue_job = glue.CfnJob(self, "GlueETLJob",
            name="prod-S3Pull-CSVParse-DDBStore",
            role=glue_role.role_arn,
            command={
                "name": "glueetl",
                "python_version": "3",
                "script_location": glue_script_path
            },
            default_arguments={
                "--TempDir": f"s3://{temp_bucket.bucket_name}/temp/",
                "--input_bucket": beta_bucket_name,
            },
            max_capacity=10.0,  # Adjust to minimize costs
            worker_type="Standard",
            number_of_workers=2
        )

        # Lambda function to trigger the Glue job
        trigger_glue_lambda = lambda_.Function(self, "TriggerGlueJobLambda",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="lambda_code.data_migration.lambda_handler",
            code=lambda_.Code.from_asset("data_migration/lambda_code"),  # Local folder for Lambda code
            environment={
                'BUCKET_NAME': beta_bucket_name,
                'GLUE_JOB_NAME': glue_job.name
            }
        )

        # Grant Lambda permissions to start the Glue job
        trigger_glue_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=["glue:StartJobRun"],
                resources=[f"arn:aws:glue:{prod_region}:{prod_account_id}:job/{glue_job.name}"]
            )
        )

        # Grant Glue role permissions to use the temporary bucket
        temp_bucket.grant_read_write(glue_role)

        # Add cross-account bucket policy for Beta S3 bucket
        cross_account_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": f"arn:aws:iam::{beta_account_id}:role/GlueJobRole"
                    },
                    "Action": ["s3:GetObject", "s3:ListBucket"],
                    "Resource": [
                        f"arn:aws:s3:::{beta_bucket_name}",
                        f"arn:aws:s3:::{beta_bucket_name}/*"
                    ]
                }
            ]
        }

        # Apply the bucket policy using a custom resource
        cr.AwsCustomResource(self, "CrossAccountBucketPolicy",
            on_create={
                "service": "S3",
                "action": "putBucketPolicy",
                "parameters": {
                    "Bucket": beta_bucket_name,
                    "Policy": json.dumps(cross_account_policy)
                }
            },
            policy=cr.AwsCustomResourcePolicy.from_statements([
                iam.PolicyStatement(
                    actions=["s3:PutBucketPolicy"],
                    resources=[f"arn:aws:s3:::{beta_bucket_name}"],
                )
            ])
        )

        # Output the Glue job and Lambda function details
        CfnOutput(self, "GlueJobName", value=glue_job.name)
        CfnOutput(self, "TriggerLambdaARN", value=trigger_glue_lambda.function_arn)
        CfnOutput(self, "TempBucketName", value=temp_bucket.bucket_name)
