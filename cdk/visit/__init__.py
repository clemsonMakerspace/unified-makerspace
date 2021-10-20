
from aws_cdk import (
    aws_s3_deployment,
    core,
    aws_cloudfront,
    aws_cloudfront_origins,
    aws_lambda,
    aws_s3,
)


class Visit(core.Stack):
    """
    Track visitors to the makerspace via a simple web console.

    This stack contains a few primary parts:

    1. A static web page asks for a Clemson username (visit.cumaker.space)
    2. An API Gateway routes requests to AWS Lambda
    3. The lambda function checks if the user has registered before
        a. If the user has registered, we just continue
        b. If the user hasn't registered, we send them an email
    4. The Lambda function records a visit in DynamoDB
    5. The registration email contains a federated link to another webpage
        (register.cumaker.space) which will be a different stack
    """

    def __init__(self, scope: core.Construct,
                 stage: str, table_name: str, **kwargs):

        super().__init__(scope, f'Visitors-{stage}', **kwargs)

        self.source_bucket()

        # todo: restrict visitors page to require employee sign-in
        # self.cognito_pool()

        self.cloudfront_distribution()

        self.register_visit_api_gateway()

        self.register_visit_lambda(table_name)

    def source_bucket(self):
        self.oai = aws_cloudfront.OriginAccessIdentity(self, 'VisitorsOriginAccessIdentity')

        self.bucket = aws_s3.Bucket(self, 'cumakerspace-visitors-console')

        self.bucket.grant_read(self.oai)

        aws_s3_deployment.BucketDeployment(self, 'VisitorsConsoleDeployment',
                                           sources=[
                                               aws_s3_deployment.Source.asset('visit/console/')
                                            ],
                                           destination_bucket=self.bucket)

    def cloudfront_distribution(self):
        aws_cloudfront.Distribution(self, 'VisitorsConsoleCache',
                                    default_behavior=aws_cloudfront.BehaviorOptions(
                                        origin=aws_cloudfront_origins.S3Origin(
                                            bucket=self.bucket,
                                            origin_access_identity=self.oai
                                        ),
                                        viewer_protocol_policy=aws_cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS),
                                        default_root_object="index.html")

    def register_visit_api_gateway(self):

        # todo: create api gateway

        pass

    def register_visit_lambda(self, table_name: str):

        aws_lambda.Function(self,
                            'RegisterVisitLambda',
                            code=aws_lambda.Code.from_asset(
                                'visit/lambda_code'),
                            environment={
                                'TABLE_NAME': table_name,
                            },
                            handler='register_visit.handler',
                            runtime=aws_lambda.Runtime.PYTHON_3_9)
