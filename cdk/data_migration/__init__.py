from aws_cdk import core
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_iam as iam
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_glue as glue
from aws_cdk import aws_logs as logs
from aws_cdk import custom_resources as cr
import json

#! WIP
class DataMigrationStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, *, env: core.Environment) -> None:
        super().__init__(scope, id, env=env)

        # 1. Use an already existing S3 bucket for input files (CSV files)
        input_bucket = s3.Bucket.from_bucket_name(self, "ExistingBucket", "testing-trigger-for-glue-job")

        # 2. Define the IAM role for the Glue job (created in Prod environment)
        glue_role = iam.Role(self, "GlueJobRole",
            assumed_by=iam.ServicePrincipal("glue.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSGlueServiceRole"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"),
            ]
        )

        # 3. Define the Glue ETL job
        glue_job = glue.CfnJob(self, "GlueETLJob",
            name="beta-S3Pull-CSVParse-DDBStore",  # The Glue job name
            role=glue_role.role_arn,  # Role created in Prod environment
            command={
                "name": "glueetl",
                "script_location": "s3://path-to-your-glue-script/script.py",  # Replace with your Glue script location
            },
            default_arguments={
                "--TempDir": f"s3://{input_bucket.bucket_name}/temp/",
                "--input_bucket": input_bucket.bucket_name,
            },
            max_capacity=10.0,  # Adjust for cost optimization (keep it as low as possible)
            worker_type="Standard",  # Use standard worker type to minimize cost
            number_of_workers=2  # Adjust based on the size of your data
        )

        # 4. Create the Lambda function that will trigger the Glue job in the Prod account
        trigger_glue_lambda = lambda_.Function(self, "TriggerGlueJobLambda",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="data_migration.lambda_handler",
            code=lambda_.Code.from_asset("lambda_code/data_migration.py"),  # Lambda code directory
            environment={
                'BUCKET_NAME': input_bucket.bucket_name,
            }
        )

        # 5. Grant Lambda function permissions to read from the S3 bucket in Beta account
        input_bucket.grant_read(trigger_glue_lambda)

        # 6. Grant Lambda function permissions to start the Glue job
        trigger_glue_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=["glue:StartJobRun"],
                resources=[f"arn:aws:glue:{core.Aws.REGION}:{core.Aws.ACCOUNT_ID}:job/beta-S3Pull-CSVParse-DDBStore"]
            )
        )

        # 7. Create a Custom Resource to modify the S3 bucket policy in the Beta account
        custom_resource = cr.AwsCustomResource(self, "CustomBucketPolicyResource",
            on_create={
                "service": "S3",
                "action": "putBucketPolicy",
                "parameters": {
                    "Bucket": input_bucket.bucket_name,
                    "Policy": json.dumps({
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Effect": "Allow",
                                "Principal": {
                                    "AWS": f"arn:aws:iam::{core.Aws.ACCOUNT_ID}:role/{trigger_glue_lambda.role.role_name}"  # Referencing the Lambda role in Prod
                                },
                                "Action": "s3:GetObject",
                                "Resource": f"arn:aws:s3:::{input_bucket.bucket_name}/*"
                            }
                        ]
                    })
                },
                "physical_resource_id": cr.PhysicalResourceId.of(input_bucket.bucket_name),
            },
            policy=cr.AwsCustomResourcePolicy.from_statements([
                iam.PolicyStatement(
                    actions=["s3:PutBucketPolicy"],
                    resources=[f"arn:aws:s3:::{input_bucket.bucket_name}"],
                ),
            ])
        )

        # 8. Output Lambda ARN and Glue Job ARN for reference
        core.CfnOutput(self, "TriggerGlueLambdaARN", value=trigger_glue_lambda.function_arn)
        core.CfnOutput(self, "GlueJobName", value=glue_job.name)
