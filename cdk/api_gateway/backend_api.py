
# from distutils.command.build import build
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
import logging

class BackendApi(core.Stack):
    """
    Consolidates all api methods for storing and retrieving data to and from
    the chosen storage solution.

    This stack contains a few primary parts:

    1. An API Gateway routes requests to AWS Lambda
    2. The lambda functions handle various requests:
        a. Handling user information
        b. Handling logging visits
        c. Handling logging equipment form submissions
        d. Handling user completion of trainings, waivers, etc.
    """

    def __init__(self, scope: core.Construct,
                 stage: str,
                 users_table_name: str,
                 visits_table_name: str,
                 equipment_table_name: str,
                 qualifications_table_name: str,
                 *,
                 env: core.Environment,
                 zones: MakerspaceDns = None):

        super().__init__(scope, 'BackendApi', env=env)
        
        # Sets up CloudWatch logs and sets level to INFO
        # self.logger = logging.getLogger()
        # self.logger.setLevel(logging.INFO)

        self.stage = stage
        self.zones = zones

        self.domain_name = self.distribution.domain_name if stage == 'Dev' else self.zones.visit.zone_name

        self.endpoint: str = "https://" + self.domain_name

        # Provision lambda functions
        self.visits_handler_lambda(visits_table_name, users_table_name, ("https://" + self.domain_name))
        self.users_handler_lambda(users_table_name, ("https://" + self.domain_name))
        self.qualifications_handler_lambda(qualifications_table_name, ("https://" + self.domain_name))
        self.equipment_handler_lambda(equipment_table_name, ("https://" + self.domain_name))

        # Create policy with AWSInvokeFullAccess actions - should work the same way
        self.api_invoke_policy = aws_iam.PolicyStatement(
            actions=["execute-api:Invoke", "execute-api:ManageConnections"],
            resources=["*"]
        )
        
        # Giving lambda functions the invoke full access policy
        self.lambda_visits_handler.role.add_to_policy(self.api_invoke_policy)
        self.lambda_users_handler.role.add_to_policy(self.api_invoke_policy)
        self.lambda_qualifications_handler.role.add_to_policy(self.api_invoke_policy)
        self.lambda_equipment_handler.role.add_to_policy(self.api_invoke_policy)
        
        # Prepare lambda testing suite #! Must recreate testing
        # self.test_api_lambda(env=stage)

    def visits_handler_lambda(self, visits_table_name: str, users_table_name: str, domain_name: str):

        self.lambda_visits_handler = aws_lambda.Function(
            self,
            'VisitsHandlerLambda',
            function_name=core.PhysicalName.GENERATE_IF_NEEDED,
            code=aws_lambda.Code.from_asset('api_gateway/lambda_code/visits_handler'),
            environment={
                'DOMAIN_NAME': domain_name,
                'VISITS_TABLE_NAME': visits_table_name,
                'USERS_TABLE_NAME': users_table_name,
            },
            handler='visits_handler.handler',
            runtime=aws_lambda.Runtime.PYTHON_3_9)

    
    def users_handler_lambda(self, users_table_name: str, domain_name: str):

        self.lambda_users_handler = aws_lambda.Function(
            self,
            'UsersHandlerLambda',
            function_name=core.PhysicalName.GENERATE_IF_NEEDED,
            code=aws_lambda.Code.from_asset('api_gateway/lambda_code/users_handler'),
            environment={
                'DOMAIN_NAME': domain_name,
                'USERS_TABLE_NAME': users_table_name,
            },
            handler='users_handler.handler',
            runtime=aws_lambda.Runtime.PYTHON_3_9)

    
    def qualifications_handler_lambda(self, qualifications_table_name: str, domain_name: str):
        
        self.lambda_qualifications_handler = aws_lambda.Function(
            self,
            'QualificationsHandlerLambda',
            function_name=core.PhysicalName.GENERATE_IF_NEEDED,
            code=aws_lambda.Code.from_asset('api_gateway/lambda_code/qualifications_handler'),
            environment={
                'DOMAIN_NAME': domain_name,
                'QUALIFICATIONS_TABLE_NAME': qualifications_table_name,
            },
            handler='qualifications_handler.handler',
            runtime=aws_lambda.Runtime.PYTHON_3_9)

    
    def equipment_handler_lambda(self, equipment_table_name: str, domain_name: str):
        
        self.lambda_equipment_handler = aws_lambda.Function(
            self,
            'EquipmentHandlerLambda',
            function_name=core.PhysicalName.GENERATE_IF_NEEDED,
            code=aws_lambda.Code.from_asset('api_gateway/lambda_code/equipment_handler'),
            environment={
                'DOMAIN_NAME': domain_name,
                'EQUIPMENT_TABLE_NAME': equipment_table_name,
            },
            handler='equipment_handler.handler',
            runtime=aws_lambda.Runtime.PYTHON_3_9)
    
    
    #! Recreate Testing Lambda Function
    def test_backend_api_lambda(self, env: str):

        self.lambda_backend_api_test = aws_lambda.Function(
            self,
            'TestBackendAPILambda',
            function_name=core.PhysicalName.GENERATE_IF_NEEDED,
            code=aws_lambda.Code.from_asset('api_gateway/lambda_code/test_backend_api'),
            environment={
                'ENV': env
            },
            handler='test_api.handler',
            runtime=aws_lambda.Runtime.PYTHON_3_9)
