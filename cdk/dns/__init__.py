
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
    Register the DNS used by the portions of the makerspace website owned by
    the capstone in Route53.

    The DNS for the rest of the makerspace is in Gandi, where we have a
    record delegating to the Route53 nameservers created by these zones.

    The biggest benefit of having Route53 manage the DNS for the maintenance
    and visitor login apps is that we can handle the TLS certs in AWS with
    fewer steps.
    
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
