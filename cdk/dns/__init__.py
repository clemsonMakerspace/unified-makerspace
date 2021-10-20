
from aws_cdk import (
    aws_route53,
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

    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.visitors_zone()

        self.maintenance_zone()

        # todo: deprecate this
        self.admin_zone()

    def visitors_zone(self):

        aws_route53.PublicHostedZone(self, 'visit',
                                     zone_name='visit.cumaker.space')

    def maintenance_zone(self):

        aws_route53.PublicHostedZone(self, 'maintenance',
                                     zone_name='maintenance.cumaker.space')

    def admin_zone(self):

        aws_route53.PublicHostedZone(self, 'admin',
                                     zone_name='admin.cumaker.space')
