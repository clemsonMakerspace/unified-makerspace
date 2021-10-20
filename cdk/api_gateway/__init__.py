
from aws_cdk import (
    core,
    aws_lambda,
    aws_apigateway,
)


class SharedApiGateway(core.Stack):
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

    def __init__(self, scope: core.Construct, stage: str,
                 visitors: aws_lambda.Function, **kwargs):

        super().__init__(scope, f'SharedApiGateway-{stage}', **kwargs)

        self.create_rest_api()

        self.route_visitors(visitors)

    def create_rest_api(self):

        self.api = aws_apigateway.RestApi(self, 'SharedApiGateway')

    def route_visitors(self, visitors: aws_lambda.Function):

        register_visit = aws_apigateway.LambdaIntegration(visitors)

        self.visit = self.api.root.add_resource('visit')

        self.visit.add_method('POST', register_visit)
