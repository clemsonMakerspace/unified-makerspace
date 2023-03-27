from aws_cdk import (
    core,
    aws_s3
)

class LogStorage(core.Stack):
    def __init__(self, scope: core.Construct,
                 stage: str, *, env: core.Environment):  
              
        super().__init__(scope, f'LogStorage-{stage}', env=env)


        self.s3_log_bucket()


        
    def s3_log_bucket(self):
        self.log_bucket = aws_s3.Bucket(self, 'quicksight-log-data',
                        block_public_access=aws_s3.BlockPublicAccess.BLOCK_ALL,
                        encryption=aws_s3.BucketEncryption.S3_MANAGED,
                        versioned=False,
                        enforce_ssl=True,
                        removal_policy=core.RemovalPolicy.DESTROY)

