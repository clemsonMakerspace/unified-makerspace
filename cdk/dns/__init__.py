
from typing import NamedTuple
from aws_cdk import (App, Stack, Stage, Environment,     
    aws_apigateway,
    aws_cloudfront,
    aws_route53,
    aws_route53_targets)
from constructs import Construct

class Domains:
    def __init__(self, stage: str):

        stage = stage.lower()
        if stage == 'prod':
            self.stage = ''
        else:
            # We can use sub-domains with NS records if we replace this
            # with 'stage.' and point the domains in the prod account
            # at the beta account nameservers.
            self.stage = f'{stage}-'

        self.api = self.domain('api')
        self.visit = self.domain('visit')
        self.maintenance = self.domain('maintenance')
        self.admin = self.domain('admin')

    def domain(self, prefix: str) -> str:
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
    """

    def __init__(self, scope: Construct,
                 stage: str, *, env: Environment):
        super().__init__(scope, f'MakerspaceDns-{stage}', env=env)

        self.domains = Domains(stage)

        self.visitors_zone()

        self.api_zone()

        self.maintenance_zone()

        # todo: deprecate this
        self.admin_zone()

    def visitors_zone(self):

        self.visit = aws_route53.PublicHostedZone(self, 'visit',
                                                  zone_name=self.domains.visit)

    def api_zone(self):

        self.api = aws_route53.PublicHostedZone(self, 'api',
                                                zone_name=self.domains.api)

    def maintenance_zone(self):

        aws_route53.PublicHostedZone(self, 'maintenance',
                                     zone_name=self.domains.maintenance)

    def admin_zone(self):

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

        id = f'MakerspaceDnsRecords-{stage}'
        super().__init__(scope, id, env=env)

        self.zones = zones

        self.add_dependency(self.zones)

        self.api_record(api_gateway)

        self.visit_record(visit_distribution)

    def api_record(self, api_gateway: aws_apigateway.RestApi):

        zone = aws_route53.HostedZone.from_hosted_zone_attributes(self,
                                                                  'ApiHostedZoneRef',
                                                                  hosted_zone_id=self.zones.api.hosted_zone_id,
                                                                  zone_name=self.zones.api.zone_name)

        aws_route53.ARecord(self, 'ApiRecord',
                            zone=zone,
                            target=aws_route53.RecordTarget(
                                alias_target=aws_route53_targets.ApiGatewayDomain(
                                    api_gateway.domain_name)))

    def visit_record(self, visit: aws_cloudfront.Distribution):

        zone = aws_route53.HostedZone.from_hosted_zone_attributes(self,
                                                                  'VisitHostedZoneRef',
                                                                  hosted_zone_id=self.zones.visit.hosted_zone_id,
                                                                  zone_name=self.zones.visit.zone_name)

        distribution = aws_cloudfront.Distribution.from_distribution_attributes(self,
                                                                                'VisitCloudFrontRef',
                                                                                distribution_id=visit.distribution_id,
                                                                                domain_name=visit.distribution_domain_name)

        aws_route53.ARecord(self, 'VisitRecord',
                            zone=zone,
                            target=aws_route53.RecordTarget(
                                alias_target=aws_route53_targets.CloudFrontTarget(
                                    distribution=distribution)))
