from aws_cdk import (
    aws_s3,
    aws_iam,
    App, Stack, Stage, Environment, RemovalPolicy
)
from constructs import Construct

class LogStorage(Stack):
    def __init__(self, scope: Construct,
                 stage: str, *, env: Environment):  
              
        super().__init__(scope, f'LogStorage-{stage}', env=env)


        self.s3_log_bucket()


        
    def s3_log_bucket(self):
        self.log_bucket = aws_s3.Bucket(self, 'quicksight-log-data',
                        block_public_access=aws_s3.BlockPublicAccess.BLOCK_ALL,
                        encryption=aws_s3.BucketEncryption.S3_MANAGED,
                        versioned=False,
                        enforce_ssl=True,
                        removal_policy=RemovalPolicy.DESTROY)
        
    def log_access_user(self):
        # Create an IAM user 
        self.log_iam_user = aws_iam.User(self, 'cdk-log-s3-user')

        # Create an S3 policy that allows read/write access to the log bucket
        s3_policy = aws_iam.PolicyStatement(
            actions=[
                's3:GetObject',
                's3:PutObject',
                's3:DeleteObject'
            ],
            resources=[
                self.log_bucket.arn_for_objects('*'),
                self.log_bucket.bucket_arn
            ]
        )

        # Create an IAM policy from the policy statement
        policy = aws_iam.Policy(
            self, "S3LogBucketAccess",
            policy_name="S3LogBucketAccess",
            statements=[s3_policy]
        )

        # Attach the S3 policy to the user
        policy.attach_to_user(self.log_iam_user)


