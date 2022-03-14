
from aws_cdk import (
    aws_certificatemanager,
    aws_s3_deployment,
    core,
    aws_cloudfront,
    aws_cloudfront_origins,
    aws_lambda,
    aws_s3,
    aws_iam,
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
                 visits_table_name: str,
                 users_table_name: str,
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

        self.log_visit_lambda(visits_table_name, users_table_name)
        self.register_user_lambda(users_table_name)

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
            kwargs['certificate'] = aws_certificatemanager.DnsValidatedCertificate(
                self, 'VisitorsCertificate', domain_name=domain_name, hosted_zone=self.zones.visit)

        kwargs['default_behavior'] = aws_cloudfront.BehaviorOptions(
            origin=aws_cloudfront_origins.S3Origin(
                bucket=self.bucket,
                origin_access_identity=self.oai),
            viewer_protocol_policy=aws_cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS)
        kwargs['default_root_object'] = "index.html"

        kwargs['price_class'] = aws_cloudfront.PriceClass.PRICE_CLASS_100

        # This error response redirect back to index.html because React handles everything in a page
        # including routing. when you add /register after the domain, there would be such key avaliable
        # in the static site. We need cloudfront redirect it back to index.html for React to
        # handle the routing.
        kwargs['error_responses'] = [aws_cloudfront.ErrorResponse(
            http_status=404,
            response_http_status=200,
            response_page_path="/index.html",
            ttl=core.Duration.seconds(10)
        )]

        self.distribution = aws_cloudfront.Distribution(
            self, 'VisitorsConsoleCache', **kwargs)

    def log_visit_lambda(self, visits_table_name: str, users_table_name: str):

        sending_authorization_policy = aws_iam.PolicyStatement(
            effect=aws_iam.Effect.ALLOW)
        sending_authorization_policy.add_actions("ses:SendEmail")
        sending_authorization_policy.add_all_resources()

        self.lambda_visit = aws_lambda.Function(
            self,
            'RegisterVisitLambda',
            function_name=core.PhysicalName.GENERATE_IF_NEEDED,
            code=aws_lambda.Code.from_asset('visit/lambda_code/log_visit'),
            environment={
                'TABLE_NAME': visits_table_name,
                'VISITS_TABLE_NAME': visits_table_name,
                'USERS_TABLE_NAME': users_table_name
            },
            handler='log_visit.handler',
            runtime=aws_lambda.Runtime.PYTHON_3_9)

        self.lambda_visit.role.add_to_policy(sending_authorization_policy)

    def register_user_lambda(self, table_name: str):

        self.lambda_register = aws_lambda.Function(
            self,
            'RegisterUserLambda',
            function_name=core.PhysicalName.GENERATE_IF_NEEDED,
            code=aws_lambda.Code.from_asset('visit/lambda_code/register_user'),
            environment={
                'TABLE_NAME': table_name,
            },
            handler='register_user.handler',
            runtime=aws_lambda.Runtime.PYTHON_3_9)
