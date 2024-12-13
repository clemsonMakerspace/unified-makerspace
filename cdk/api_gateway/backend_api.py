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
    The BackendApi stack consolidates all Lambda functions responsible for storing 
    and retrieving data to and from the application's storage solution. These functions 
    are designed to handle various API Gateway requests for user information, visit logs, 
    equipment usage, and training data.

    Purpose
    ---
    This stack provides the backend infrastructure for managing API requests via AWS Lambda. 
    It integrates with DynamoDB tables for data persistence and uses environment variables 
    to pass configuration details such as table names and domain endpoints.

    Structure
    ---
    The stack includes the following components:
    1. Lambda Functions:
        - **Visits Handler**: Manages visit logs.
        - **Users Handler**: Handles user information.
        - **Qualifications Handler**: Tracks user progress in training programs.
        - **Equipment Handler**: Manages equipment usage logs.
        - **Tiger Training Handler**: Integrates with Bridge LMS to manage training data.
    2. IAM Policies:
        - Grants all Lambda functions the `execute-api:Invoke` and `execute-api:ManageConnections` actions.
    3. Integration with External Services:
        - Uses AWS Secrets Manager to securely retrieve credentials for Bridge LMS integration.

    Parameters:
    - scope (Construct): The scope in which this construct is defined.
    - stage (str): The deployment stage (e.g., "prod", "beta").
    - users_table_name (str): The name of the DynamoDB table for user data.
    - visits_table_name (str): The name of the DynamoDB table for visit logs.
    - equipment_table_name (str): The name of the DynamoDB table for equipment usage logs.
    - qualifications_table_name (str): The name of the DynamoDB table for training qualifications.
    - env (Environment): The AWS environment, including account and region.
    - zones (MakerspaceDns): Optional Makerspace DNS configuration.

    Key Features:
    - **Lambda Function Provisioning**:
        - Dynamically provisions Lambda functions for each API endpoint.
        - Configures environment variables with table names and other settings.
    - **IAM Policies**:
        - Adds a policy to all Lambda functions to allow `execute-api:Invoke` and `execute-api:ManageConnections`.
    - **Integration with Bridge LMS**:
        - Uses AWS Secrets Manager to securely fetch API keys and credentials for the Tiger Training handler.
    - **Environment-Specific Configuration**:
        - Configures the API endpoint based on the deployment stage and DNS settings.

    Notes:
    - The Tiger Training handler is created last to ensure dependencies, such as the qualifications handler's 
      function name, are resolved.

    Documentation Links:
        - aws_lambda.Function:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html
        - aws_iam.PolicyStatement:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_iam/PolicyStatement.html
        - aws_secretsmanager.Secret:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_secretsmanager/Secret.html
        - aws_lambda.Code:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Code.html
        - aws_lambda.Runtime:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Runtime.html
        - aws_lambda.EnvironmentVariable:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/EnvironmentVariable.html
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

        # Allow tiger training to invoke qualifications
        self.lambda_qualifications_handler.grant_invoke(self.lambda_tiger_training_handler)


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
                'BRIDGE_KEY': bridge_key.to_string(),
                'BRIDGE_SECRET': bridge_secret.to_string(),
                'BRIDGE_PROGRAM_ID': makerspace_program_id,
                'QUALIFICATIONS_LAMBDA': self.lambda_qualifications_handler.function_name
            },
            handler='tiger_training_handler.handler',
            timeout=Duration.seconds(30),
            runtime=aws_lambda.Runtime.PYTHON_3_12)

        bridge_secrets.grant_read(self.lambda_tiger_training_handler)
