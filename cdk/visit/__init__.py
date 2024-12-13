
# from distutils.command.build import build
from aws_cdk import (
    Stack,
    Environment,
    aws_certificatemanager,
    aws_s3_deployment,
    aws_cloudfront,
    aws_cloudfront_origins,
    aws_lambda,
    aws_s3,
    aws_iam,
    aws_secretsmanager,
    Duration,
    Aws,
    PhysicalName
)
from constructs import Construct
from dns import MakerspaceDns
import logging

class Visit(Stack):
    """
    The Visit stack tracks visitors to the Makerspace through a simple web console.
    This stack provides a backup mechanism for visitor registration in case the 
    hardware scanner is unavailable.

    Workflow:
    1. A static web page (e.g., `visit.cumaker.space`) asks for the Clemson username.
    2. A backend API call logs the visit.
    3. Additional registration logic is handled by the visits handler.
    4. The visit is successfully logged.

    Parameters:
    - scope (Construct): The scope in which this construct is defined.
    - stage (str): The deployment stage (e.g., "prod", "beta", "dev").
    - env (Environment): The AWS environment in which the stack is deployed.
    - create_dns (bool): Whether to create DNS entries for the application.
    - zones (MakerspaceDns): An optional instance of the `MakerspaceDns` stack to manage DNS zones.

    Key Features:
    - **Source Bucket**:
        - Creates an S3 bucket for storing static website assets.
        - Grants read access to a CloudFront Origin Access Identity (OAI).
        - Deploys static files from the local directory (`visit/console/{stage}/`) to the S3 bucket.
    - **CloudFront Distribution**:
        - Configures a CloudFront distribution for the static site.
        - Supports HTTPS with a certificate (if `create_dns` is `True`).
        - Redirects HTTP requests to HTTPS.
        - Handles 404 errors by redirecting to `index.html` for React-based routing.
        - Uses `PRICE_CLASS_100` for cost optimization.

    Methods:
    - source_bucket():
        - Creates an S3 bucket for static assets.
        - Grants CloudFront OAI read access to the bucket.
        - Deploys static files to the bucket using `BucketDeployment`.
    - cloudfront_distribution():
        - Configures a CloudFront distribution for the static site.
        - Optionally associates a domain name and SSL certificate (if `create_dns` is `True`).

    Notes:
    - The `create_dns` parameter controls whether DNS records and SSL certificates are set up.
    - The error handling ensures compatibility with React routing by redirecting all paths to `index.html`.
    - Static files for deployment must be placed in `visit/console/{stage}/`.

    Documentation Links:
        - aws_s3.Bucket:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_s3/Bucket.html
        - aws_cloudfront.Distribution:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cloudfront/Distribution.html
        - aws_s3_deployment.BucketDeployment:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_s3_deployment/BucketDeployment.html
        - aws_certificatemanager.Certificate:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_certificatemanager/Certificate.html
    """

    def __init__(self, scope: Construct,
                 stage: str,
                 *,
                 env: Environment,
                 create_dns: bool,
                 zones: MakerspaceDns = None):

        super().__init__(scope, 'Visitors', env=env)
        
        # Sets up CloudWatch logs and sets level to INFO
        # self.logger = logging.getLogger()
        # self.logger.setLevel(logging.INFO)

        self.stage = stage
        self.create_dns = create_dns
        self.zones = zones

        self.source_bucket()

        self.cloudfront_distribution()


    def source_bucket(self):
        self.oai = aws_cloudfront.OriginAccessIdentity(
            self, 'VisitorsOriginAccessIdentity')
 
        self.bucket = aws_s3.Bucket(self, 'cumakerspace-visitors-console')
        self.bucket.grant_read(self.oai)

        # Deploy static files to the bucket
        aws_s3_deployment.BucketDeployment(
            self,
            'VisitorsConsoleDeployment',
            sources=[
                aws_s3_deployment.Source.asset(f'visit/console/{self.stage}/')
            ],
            destination_bucket=self.bucket
        )
        
    def cloudfront_distribution(self):

        kwargs = {}

        if self.create_dns:
            domain_name = self.zones.visit.zone_name
            kwargs['domain_names'] = [domain_name]
            kwargs['certificate'] = aws_certificatemanager.Certificate(
                self,
                'VisitorsCertificate',
                domain_name=domain_name,
                validation=aws_certificatemanager.CertificateValidation.from_dns(self.zones.visit)
            )

        # Configure default behavior
        kwargs['default_behavior'] = aws_cloudfront.BehaviorOptions(
            origin=aws_cloudfront_origins.S3Origin(
                self.bucket,
                origin_access_identity=self.oai
            ),
            viewer_protocol_policy=aws_cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
        )

        kwargs['default_root_object'] = "index.html"
        kwargs['price_class'] = aws_cloudfront.PriceClass.PRICE_CLASS_100

        # This error response redirect back to index.html because React handles everything in a page
        # including routing. when you add /register after the domain, there would be such key avaliable
        # in the static site. We need cloudfront redirect it back to index.html for React to
        # handle the routing.
        kwargs['error_responses'] = [
            aws_cloudfront.ErrorResponse(
                http_status=404,
                response_http_status=200,
                response_page_path="/index.html",
                ttl=Duration.seconds(10)
            )
        ]

        # Create CloudFront Distribution
        self.distribution = aws_cloudfront.Distribution(
            self, 'VisitorsConsoleCache', **kwargs
        )
