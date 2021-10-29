
from aws_cdk import (
    aws_apigateway,
    aws_cloudfront,
    aws_route53,
    aws_route53_targets,
    core
)


class MakerspaceDns(core.Stack):
    """
    Register the DNS used by the portions of the makerspace website owned by
    the capstone in Route53.

    The DNS for the rest of the makerspace is in Gandi, where we have a
    record delegating to the Route53 nameservers created by these zones.

    The biggest benefit of having Route53 manage the DNS for the maintenance
    and visitor login apps is that we can handle the TLS certs in AWS with
    fewer steps.
    """

    def __init__(self, scope: core.Construct, id: str,
                 visitors_cf_domain: aws_cloudfront.Distribution,
                 api_domain: aws_apigateway.RestApi,
                 **kwargs):
        super().__init__(scope, id, **kwargs)

        self.visitors_zone(visitors_cf_domain)

        self.api_zone(api_domain)

        self.maintenance_zone()

        # todo: deprecate this
        self.admin_zone()

    def visitors_zone(self, cf_domain):

        self.visits = aws_route53.PublicHostedZone(self, 'visit',
                                                   zone_name='visit.cumaker.space')

        aws_route53.ARecord(self, 'VisitRecord',
                            zone=self.visits,
                            target=aws_route53.RecordTarget(
                                alias_target=aws_route53_targets.CloudFrontTarget(
                                    cf_domain)))

    def api_zone(self, api_domain: aws_apigateway.RestApi):

        self.api = aws_route53.PublicHostedZone(self, 'api',
                                                zone_name='api.cumaker.space')

        aws_route53.ARecord(self, 'ApiRecordRecord',
                            zone=self.api,
                            target=aws_route53.RecordTarget(
                                alias_target=aws_route53_targets.ApiGatewayDomain(
                                    api_domain.domain_name)))

    def maintenance_zone(self):

        aws_route53.PublicHostedZone(self, 'maintenance',
                                     zone_name='maintenance.cumaker.space')

    def admin_zone(self):

        aws_route53.PublicHostedZone(self, 'admin',
                                     zone_name='admin.cumaker.space')
