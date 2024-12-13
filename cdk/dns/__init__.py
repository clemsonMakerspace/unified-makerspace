
from typing import NamedTuple
from aws_cdk import (
    Stack,
    Environment,
    aws_apigateway,
    aws_cloudfront,
    aws_route53,
    aws_route53_targets,
    aws_certificatemanager
)
from constructs import Construct


class Domains:
    """
    The Domains class generates domain names based on the deployment stage. These domains
    are used for configuring hosted zones and DNS records in the Makerspace DNS stack.

    This class ensures consistent domain naming for various services, such as:
    - API
    - Visitor login
    - Maintenance and admin (partially set up, can be extended).

    Parameters:
    - stage (str): The deployment stage (e.g., "prod", "beta", "dev"). The stage determines
                   the domain name prefixes. For production, no prefix is added.

    Attributes:
    - api (str): The domain name for the API service (e.g., "api.cumaker.space").
    - visit (str): The domain name for the visitor login service (e.g., "visit.cumaker.space").
    - maintenance (str): The domain name for maintenance services.
    - admin (str): The domain name for admin services.

    Methods:
    - domain(prefix: str) -> str:
        Constructs a domain name using the provided prefix and the current stage.

    Notes:
    - To expand for other schools or spaces, modify the `domain` method to support additional patterns.
    """
    def __init__(self, stage: str):

        stage = stage.lower()
        if stage == 'prod':
            # Prepend with nothing - we want normal sub-domains
            # i.e. visit.cumaker.space, not prod-visit.cumaker.space
            self.stage = ''
        else:
            # We can use sub-domains with NS records if we replace this
            # with 'stage.' and point the domains in the prod account
            # at the beta account nameservers.
            self.stage = f'{stage}-'

        self.api = self.domain('api')
        self.visit = self.domain('visit')
        
        # We current do not use these but they are partially setup.
        # If you want to use these, add a way to add A 
        # records for these in the MakerspaceDnsRecords stack below.
        self.maintenance = self.domain('maintenance')
        self.admin = self.domain('admin')

    def domain(self, prefix: str) -> str:
        """ 
        Creates the strings for each domain to be utilized
        in the MakerspaceDns Stack
        """
        # todo: to expand to more schools or spaces, modify this
        return f'{self.stage}{prefix}.cumaker.space'


class MakerspaceDns(Stack):
    """
    The MakerspaceDns stack registers DNS zones in Route 53 for the Makerspace application.
    This includes creating hosted zones for services such as the API and visitor login.

    The stack also configures Route 53 to handle TLS certificates with minimal effort.

    Parameters:
    - scope (Construct): The scope in which this construct is defined.
    - stage (str): The deployment stage (e.g., "prod", "beta", "dev") used to determine domain names.
    - env (Environment): The AWS environment where the stack is deployed, including account and region.

    Key Features:
    - Configures Public Hosted Zones for:
        - Visitor login (`visit.cumaker.space`).
        - API (`api.cumaker.space`).
        - Maintenance and admin zones (currently unused but partially set up).
    - Supports delegation of non-production domains to the beta environment's nameservers.

    Methods:
    - visitors_zone(): Creates a hosted zone for visitor login.
    - api_zone(): Creates a hosted zone for the API service.
    - maintenance_zone(): Placeholder for creating a hosted zone for maintenance services.
    - admin_zone(): Placeholder for creating a hosted zone for admin services.

    Notes:
    - Non-production stages include prefixes (e.g., "beta-visit.cumaker.space").
    - Additional A records must be added to fully utilize maintenance and admin zones.

    Documentation Links:
        - aws_route53:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_route53.html 
        - aws_route53.PublicHostedZone: 
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_route53/PublicHostedZone.html  
        - aws_route53.ARecord:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_route53/ARecord.html
    """

    def __init__(self, scope: Construct,
                 stage: str, *, env: Environment):
        super().__init__(scope, 'MakerspaceDns', env=env)

        # Obtain domains for passed in stage
        self.domains = Domains(stage)
        
        self.visitors_zone()
        self.api_zone()

        # Currently not using these Route53 Hosted Zones
        # They are created in the case for future implmentation
        self.maintenance_zone()
        self.admin_zone()

    def visitors_zone(self):
        """ 
        Creates the Public Hosted Zone in Route53 with the passed in domain
        """
        self.visit = aws_route53.PublicHostedZone(self, 'visit',
                                                  zone_name=self.domains.visit)

    def api_zone(self):
        """ 
        Creates the Public Hosted Zone in Route53 with the passed in domain
        """
        self.api_hosted_zone = aws_route53.PublicHostedZone(self, 'api',
                                                zone_name=self.domains.api)

    def maintenance_zone(self):
        """ 
        Creates the Public Hosted Zone in Route53 with the passed in domain
        """
        aws_route53.PublicHostedZone(self, 'maintenance',
                                     zone_name=self.domains.maintenance)

    def admin_zone(self):
        """ 
        Creates the Public Hosted Zone in Route53 with the passed in domain
        """
        aws_route53.PublicHostedZone(self, 'admin',
                                     zone_name=self.domains.admin)


class MakerspaceDnsRecords(Stack):
    """
    The MakerspaceDnsRecords stack creates DNS records in Route 53 for the Makerspace application.
    These records link hosted zones to services such as the API and visitor login.

    Parameters:
    - scope (Construct): The scope in which this construct is defined.
    - stage (str): The deployment stage (e.g., "prod", "beta", "dev").
    - env (Environment): The AWS environment where the stack is deployed, including account and region.
    - zones (MakerspaceDns): An instance of the `MakerspaceDns` stack providing hosted zones.
    - api_gateway (aws_apigateway.RestApi): The API Gateway resource to be linked to the API hosted zone.
    - visit_distribution (aws_cloudfront.Distribution): The CloudFront distribution for visitor login.

    Key Features:
    - Adds DNS A records for:
        - API hosted zone (`api.cumaker.space`).
        - Visitor login hosted zone (`visit.cumaker.space`).
    - Ensures hosted zones are created before DNS records by adding a dependency on `MakerspaceDns`.

    Methods:
    - api_record(api_gateway): Creates an A record linking the API hosted zone to the API Gateway.
    - visit_record(visit_distribution): Creates an A record linking the visitor login zone to the CloudFront distribution.

    Notes:
    - Maintenance and admin zones are not fully configured but can be extended as needed.
    - A dependency ensures that hosted zones exist before records are added.

    Documentation Links:
        - aws_route53.ARecord:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_route53.ARecord.html
        - aws_route53.RecordTarget:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_route53.RecordTarget.html
        - aws_route53_targets.ApiGatewayDomain:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_route53_targets.ApiGatewayDomain.html
        - aws_route53_targets.CloudFrontTarget:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_route53_targets.CloudFrontTarget.html
    """
    def __init__(self, scope: Construct,
                 stage: str,
                 *,
                 env: Environment,
                 zones: MakerspaceDns,
                 api_gateway: aws_apigateway.RestApi,
                 visit_distribution: aws_cloudfront.Distribution):

        id = 'MakerspaceDnsRecords'
        super().__init__(scope, id, env=env)

        self.zones = zones
        
        # Adds dependency to ensure we have the zones 
        # populated prior to moving forward
        self.add_dependency(self.zones)

        # Create A Record for api Hosted Zone
        self.api_record(api_gateway)

        # Creates A Record for visit Hosted Zone
        self.visit_record(visit_distribution)

    def api_record(self, api_gateway: aws_apigateway.RestApi):

        zone = self.zones.api_hosted_zone

        # Creates A Record
        aws_route53.ARecord(self, 'ApiRecord',
                            zone=zone,
                            target=aws_route53.RecordTarget(
                                alias_target=aws_route53_targets.ApiGatewayDomain(
                                    domain_name=api_gateway.domain_name)))

    def visit_record(self, visit: aws_cloudfront.Distribution):

        zone = self.zones.visit

        # Creates A Record
        aws_route53.ARecord(self, 'VisitRecord',
                            zone=zone,
                            target=aws_route53.RecordTarget(
                                alias_target=aws_route53_targets.CloudFrontTarget(
                                    distribution=visit)))
