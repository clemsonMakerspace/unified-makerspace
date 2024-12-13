from aws_cdk import (
    Stack,
    Environment,
    aws_lambda as lambda_,
    aws_iam as iam,
    aws_glue as glue,
    aws_s3 as s3,
    custom_resources as cr,
    CfnOutput,
    RemovalPolicy
)
from constructs import Construct
import json

from ..accounts_config import accounts

class DataMigrationStack(Stack):
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

        # Read the Glue script from the local file
        with open("data_migration/glue_script.py", "r") as script_file:
            glue_script_content = script_file.read()

        # Create the Glue job
        glue_job = glue.CfnJob(self, "GlueETLJob",
            name="prod-S3Pull-CSVParse-DDBStore",
            role=glue_role.role_arn,
            command={
                "name": "glueetl",
                "python_version": "3",
                "script_location": f"inline://{glue_script_content}"  # Pass the script inline
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
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="data_migration.lambda_handler",
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
