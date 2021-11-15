
from aws_cdk import (
    aws_certificatemanager,
    aws_s3_deployment,
    core,
    aws_cloudfront,
    aws_cloudfront_origins,
    aws_lambda,
    aws_s3,
)

from dns import MakerspaceDns


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
                 stage: str,
                 table_name: str,
                 *,
                 env: core.Environment,
                 create_dns: bool,
                 zones: MakerspaceDns = None):

        super().__init__(scope, f'Visitors-{stage}', env=env)

        self.create_dns = create_dns
        self.zones = zones

        self.source_bucket()

        # todo: restrict visitors page to require employee sign-in
        # self.cognito_pool()

        self.cloudfront_distribution()

        self.register_visit_lambda(table_name)
        self.register_user_lambda(table_name)

    def source_bucket(self):
        self.oai = aws_cloudfront.OriginAccessIdentity(
            self, 'VisitorsOriginAccessIdentity')

        self.bucket = aws_s3.Bucket(self, 'cumakerspace-visitors-console')

        self.bucket.grant_read(self.oai)

        aws_s3_deployment.BucketDeployment(self, 'VisitorsConsoleDeployment',
                                           sources=[
                                               aws_s3_deployment.Source.asset(
                                                   'visit/console/')
                                           ],
                                           destination_bucket=self.bucket)

    def cloudfront_distribution(self):

        kwargs = {}
        if self.create_dns:
            domain_name = self.zones.visit.zone_name
            kwargs['domain_names'] = [domain_name]
            kwargs['certificate'] = aws_certificatemanager.DnsValidatedCertificate(self, 'VisitorsCertificate',
                                                                                   domain_name=domain_name,
                                                                                   hosted_zone=self.zones.visit)

        kwargs['default_behavior'] = aws_cloudfront.BehaviorOptions(
            origin=aws_cloudfront_origins.S3Origin(
                bucket=self.bucket,
                origin_access_identity=self.oai
            ),
            viewer_protocol_policy=aws_cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS)
        kwargs['default_root_object'] = "index.html"

        self.distribution = aws_cloudfront.Distribution(
            self, 'VisitorsConsoleCache', **kwargs)

    def register_visit_lambda(self, table_name: str):

        self.lambda_visit = aws_lambda.Function(self,
                                           'RegisterVisitLambda',
                                           function_name=core.PhysicalName.GENERATE_IF_NEEDED,
                                           code=aws_lambda.Code.from_asset(
                                               'visit/lambda_code'),
                                           environment={
                                               'TABLE_NAME': table_name,
                                           },
                                           handler='register_visit.handler',
                                           runtime=aws_lambda.Runtime.PYTHON_3_9)

    def register_user_lambda(self, table_name: str):

        self.lambda_register = aws_lambda.Function(self,
                                            'RegisterUserLambda',
                                            function_name=core.PhysicalName.GENERATE_IF_NEEDED,
                                            code=aws_lambda.Code.from_asset(
                                                'visit/lambda_code'),
                                            environment={
                                                'TABLE_NAME': table_name,
                                            },
                                            handler='register_user.handler',
                                            runtime=aws_lambda.Runtime.PYTHON_3_9)