# from distutils.command.build import build
from aws_cdk import (
    Stack,
    Environment,
    aws_lambda,
    aws_iam,
    aws_secretsmanager,
    PhysicalName,
    Duration,
    SecretValue
)
from constructs import Construct
from dns import MakerspaceDns
import logging

class BackendApi(Stack):
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

    def __init__(self, scope: Construct,
                 stage: str,
                 users_table_name: str,
                 visits_table_name: str,
                 equipment_table_name: str,
                 qualifications_table_name: str,
                 *,
                 env: Environment,
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
        self.visits_handler_lambda(visits_table_name, users_table_name, self.endpoint)
        self.users_handler_lambda(users_table_name, self.endpoint)
        self.qualifications_handler_lambda(qualifications_table_name, self.endpoint)
        self.equipment_handler_lambda(equipment_table_name, self.endpoint)

        # Tiger training handler depends on qualifications handler's function name.
        # Create last to ensure this dependency is met.
        self.tiger_training_handler_lambda(self.endpoint)

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
        self.lambda_tiger_training_handler.role.add_to_policy(self.api_invoke_policy)


    def visits_handler_lambda(self, visits_table_name: str, users_table_name: str, domain_name: str):

        self.lambda_visits_handler = aws_lambda.Function(
            self,
            'VisitsHandlerLambda',
            function_name=PhysicalName.GENERATE_IF_NEEDED,
            code=aws_lambda.Code.from_asset('api_gateway/lambda_code/visits_handler'),
            environment={
                'DOMAIN_NAME': domain_name,
                'VISITS_TABLE_NAME': visits_table_name,
                'USERS_TABLE_NAME': users_table_name
            },
            handler='visits_handler.handler',
            timeout=Duration.seconds(30),
            runtime=aws_lambda.Runtime.PYTHON_3_12)

    
    def users_handler_lambda(self, users_table_name: str, domain_name: str):

        self.lambda_users_handler = aws_lambda.Function(
            self,
            'UsersHandlerLambda',
            function_name=PhysicalName.GENERATE_IF_NEEDED,
            code=aws_lambda.Code.from_asset('api_gateway/lambda_code/users_handler'),
            environment={
                'DOMAIN_NAME': domain_name,
                'USERS_TABLE_NAME': users_table_name,
            },
            handler='users_handler.handler',
            timeout=Duration.seconds(30),
            runtime=aws_lambda.Runtime.PYTHON_3_12)

    
    def qualifications_handler_lambda(self, qualifications_table_name: str, domain_name: str):
        
        self.lambda_qualifications_handler = aws_lambda.Function(
            self,
            'QualificationsHandlerLambda',
            function_name=PhysicalName.GENERATE_IF_NEEDED,
            code=aws_lambda.Code.from_asset('api_gateway/lambda_code/qualifications_handler'),
            environment={
                'DOMAIN_NAME': domain_name,
                'QUALIFICATIONS_TABLE_NAME': qualifications_table_name,
            },
            handler='qualifications_handler.handler',
            timeout=Duration.seconds(30),
            runtime=aws_lambda.Runtime.PYTHON_3_12)

    
    def equipment_handler_lambda(self, equipment_table_name: str, domain_name: str):
        
        self.lambda_equipment_handler = aws_lambda.Function(
            self,
            'EquipmentHandlerLambda',
            function_name=PhysicalName.GENERATE_IF_NEEDED,
            code=aws_lambda.Code.from_asset('api_gateway/lambda_code/equipment_handler'),
            environment={
                'DOMAIN_NAME': domain_name,
                'EQUIPMENT_TABLE_NAME': equipment_table_name,
            },
            handler='equipment_handler.handler',
            timeout=Duration.seconds(30),
            runtime=aws_lambda.Runtime.PYTHON_3_12)


    def tiger_training_handler_lambda(self, domain_name: str):

        # Retrieve Bridge LMS key and secret
        secret_name: str = "BridgeLMSApiSecrets"
        bridge_secrets = aws_secretsmanager.Secret.from_secret_name_v2(
                self, 
                "BridgeSecrets",
                secret_name
        )
        bridge_key: SecretValue = bridge_secrets.secret_value_from_json("key")
        bridge_secret: SecretValue = bridge_secrets.secret_value_from_json("secret")

        bridge_url: str = "https://clemson.bridgeapp.com"

        # The id of the Makerspace's program in Tiger Training (Bridge LMS)
        makerspace_program_id: str = "4133"

        self.lambda_tiger_training_handler = aws_lambda.Function(
            self,
            'TigerTrainingHandlerLambda',
            function_name=PhysicalName.GENERATE_IF_NEEDED,
            code=aws_lambda.Code.from_asset('api_gateway/lambda_code/tiger_training_handler'),
            environment={
                'DOMAIN_NAME': domain_name,
                'BRIDGE_URL': bridge_url,
                'BRIDGE_KEY': bridge_key,
                'BRIDGE_SECRET': bridge_secret,
                'BRIDGE_PROGRAM_ID': makerspace_program_id,
                'QUALIFICATIONS_LAMBDA': self.lambda_qualifications_handler.function_name
            },
            handler='equipment_handler.handler',
            timeout=Duration.seconds(30),
            runtime=aws_lambda.Runtime.PYTHON_3_12)
