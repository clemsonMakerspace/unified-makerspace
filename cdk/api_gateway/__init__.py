
from aws_cdk import (
    aws_certificatemanager,
    aws_lambda,
    aws_apigateway,
)
from aws_cdk import App, Stack, Stage, Environment
from constructs import Construct
from dns import MakerspaceDns


class SharedApiGateway(Stack):
    """
    Amazon API Gateway for all Lambdas, will be fronted by `api.cumaker.space`.

    Structure
    ---

    Each API that integrates with this stack needs to be imported as a Lambda
    function. For now there's only one, but eventually we should pass them
    in in some more structured way.

    Each lambda maps to a method in this class which is responsible for
    setting up the integrations of that lambda function.

    Authorization
    ---

    This API Gateway is unsecured for now, but we'll be adding cognito authorizers
    soon. The only authorizer we care about is the cognito pool that keeps track
    of makerspace employees, because even for the visits lambda, we'll authorize
    all visitors by the employee who signed in the console.

    The user APIs for any user-facing apps could use OAuth, but we haven't gotten
    that far in the design yet.
    """

    def __init__(self, scope: Construct, stage: str,
                 visitors: aws_lambda.Function, register: aws_lambda.Function, *, env: Environment, create_dns: bool, zones: MakerspaceDns = None):

        super().__init__(scope, f'SharedApiGateway-{stage}', env=env)

        self.create_dns = create_dns
        self.zones = zones

        self.create_rest_api()

        self.route_visitors(visitors)
        self.route_registration(register)

    def create_rest_api(self):

        self.api = aws_apigateway.RestApi(self, 'SharedApiGateway')
        if self.create_dns:
            domain_name = self.zones.api.zone_name
            certificate = aws_certificatemanager.DnsValidatedCertificate(self, 'ApiGatewayCert',
                                                                         domain_name=domain_name,
                                                                         hosted_zone=self.zones.api)

            self.api.add_domain_name('ApiGatewayDomainName',
                                     domain_name=domain_name,
                                     certificate=certificate)

    def route_visitors(self, visitors: aws_lambda.Function):

        log_visit = aws_apigateway.LambdaIntegration(visitors)

        self.visit = self.api.root.add_resource('visit')

        self.visit.add_method('POST', log_visit)

    def route_registration(self, register: aws_lambda.Function):

        register_user = aws_apigateway.LambdaIntegration(register)

        self.register = self.api.root.add_resource('register')

        self.register.add_method('POST', register_user)

    def get_api(self):
        return self.api