
from aws_cdk import (
    Stage,
    Stack,
    Environment,
    aws_secretsmanager,
    SecretValue
)
from constructs import Construct

from visit import Visit
from api_gateway.shared_api_gateway import SharedApiGateway
from api_gateway.backend_api import BackendApi
from database import Database
from dns import (MakerspaceDnsRecords, MakerspaceDns, Domains)
from cognito.cognito_construct import CognitoConstruct
# from data_migration import DataMigrationStack

class MakerspaceStage(Stage):
    """
    The MakerspaceStage class defines the deployment stage for the Makerspace application.
    It is responsible for creating the `MakerspaceStack` for a specific stage (e.g., "prod", "beta").

    Parameters:
    - scope (Construct): The scope in which this construct is defined.
    - stage (str): The deployment stage (e.g., "prod", "beta").
    - env (Environment): The AWS environment, including account and region, where the stack is deployed.

    Key Features:
    - Defines the deployment pipeline by instantiating the `MakerspaceStack`.
    - Ensures consistent setup across environments.

    Documentation Links:
        - aws_cdk.Stage:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.Stage.html
    """
    def __init__(self, scope: Construct, stage: str, *,
                 env: Environment) -> None:
        super().__init__(scope, stage, env=env)
        
        self.service = MakerspaceStack(self, stage, env=env)


class MakerspaceStack(Stack):
    """
    The MakerspaceStack class sets up the infrastructure required for the Makerspace application.
    This includes all necessary resources such as databases, APIs, DNS, and authentication.

    Parameters:
    - app (Construct): The parent application or stack that this stack belongs to.
    - stage (str): The deployment stage (e.g., "prod", "beta").
    - env (Environment): The AWS environment, including account and region, where the stack is deployed.

    Key Features:
    - **Hosted Zones (DNS)**:
        - Creates Route 53 hosted zones for DNS records using the `MakerspaceDns` stack.
    - **Database**:
        - Configures DynamoDB tables for users, visits, equipment, and qualifications using the `Database` stack.
    - **Cognito**:
        - Configures an AWS Cognito User Pool and User Pool Client for authentication.
    - **API Gateway**:
        - Sets up the `SharedApiGateway` and `BackendApi` for handling API requests.
    - **Visitor Web Console**:
        - Deploys the visitor web console with an S3 bucket and CloudFront distribution using the `Visit` stack.
    - **DNS Records**:
        - Manages DNS records for the application using the `MakerspaceDnsRecords` stack.
    - **IAM Permissions**:
        - Grants Lambda functions appropriate permissions to interact with DynamoDB tables.

    Notes:
    - Dependencies are explicitly added between stacks to ensure correct order of resource provisioning.
    - DNS configuration is skipped for "dev" environments based on `create_dns` logic.

    Methods:
    - `database_stack()`: Creates the `Database` stack for DynamoDB tables.
    - `visitors_stack()`: Creates the `Visit` stack for the visitor console.
    - `backend_stack()`: Creates the `BackendApi` stack for API handling.
    - `shared_api_gateway()`: Creates the `SharedApiGateway` stack for centralized API management.
    - `hosted_zones_stack()`: Sets up Route 53 hosted zones for DNS.
    - `dns_records_stack()`: Creates DNS records for the hosted zones.
    - `cognito_setup()`: Sets up AWS Cognito for authentication.

    Documentation Links:
        - aws_cdk.Stack:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.Stack.html
        - aws_cdk.Environment:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.Environment.html
        - aws_secretsmanager.Secret:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_secretsmanager/Secret.html
        - aws_cognito.UserPool:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cognito/UserPool.html
        - aws_dynamodb.Table:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_dynamodb/Table.html
        - aws_route53.PublicHostedZone:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_route53/PublicHostedZone.html
        - aws_cloudfront.Distribution:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cloudfront/Distribution.html
        - aws_lambda.Function:
            - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html
    """
    def __init__(self, app: Construct, stage: str, *,
                 env: Environment):
        super().__init__(
            app,
            'MakerspaceStack',
            env=env,
            termination_protection=True)

        self.app = app
        self.stage = stage
        self.env = env

        # Obtain domains for passed in stage
        self.domains = Domains(self.stage)

        # Create Hosted Zones in Route53
        self.hosted_zones_stack()

        # Evaluate to true; no longer using
        # dev accounts as it was previously 
        # setup this way (Note from Fall '24)
        self.create_dns = 'dev' not in self.domains.stage

        self.database_stack()

        self.cognito_setup()
        
        # Create the backend api and shared api gateway first to obtain an api url
        self.backend_stack()

        self.shared_api_gateway()
        
        self.visitors_stack()

        if self.create_dns:
            self.dns_records_stack()

        
        # if self.stage.lower() == 'prod':
        #     self.data_migration_stack()
        
        # Set permissions for each lambda function to respective DDB table
        self.database.visits_table.grant_read_write_data(
            self.backend_api.lambda_visits_handler)

        # Both visits and users handlers need access to users table
        self.database.users_table.grant_read_data(self.backend_api.lambda_visits_handler)
        self.database.users_table.grant_read_write_data(self.backend_api.lambda_users_handler)
        
        self.database.equipment_table.grant_read_write_data(self.backend_api.lambda_equipment_handler)
        
        self.database.qualifications_table.grant_read_write_data(self.backend_api.lambda_qualifications_handler)
            
    # def data_migration_stack(self):
        
    #     self.migration = DataMigrationStack(self.app, self.stage, env=self.env)
        
    #     self.add_dependency(self.migration)
        

    def database_stack(self):
        """ 
        Creates Database Stack in CloudFormation\n
        Creates and configures each DynamoDB table we are using in our environments
        """

        self.database = Database(self.app, self.stage, env=self.env)

        # Dependency ensures this is completely configured prior
        # to continuing on
        self.add_dependency(self.database)

    def visitors_stack(self):
        """ 
        Creates the Visit Stack in CloudFormation\n
        Creates and configures the source artifact bucket for our website\n
        Creates and configures the CloudFront Distribution for global access\n
            to the website
        """

        self.visit = Visit(
            self.app,
            self.stage,
            create_dns=self.create_dns,
            zones=self.dns,
            env=self.env,
        )

        # Dependency ensures this is completely configured prior
        # to continuing on
        self.add_dependency(self.visit)

    def backend_stack(self):
        """ 
        Creates and configures all the backend api Lambda functions
            utilized by the SharedApiGateway Stack; grants the appropriate
            permissions to those functions.
        """

        self.backend_api = BackendApi(
            self.app,
            self.stage,
            self.database.users_table.table_name,
            self.database.visits_table.table_name,
            self.database.equipment_table.table_name,
            self.database.qualifications_table.table_name,
            zones=self.dns,
            env=self.env,
        )

        # Dependency ensures this is completely configured prior
        # to continuing on
        self.add_dependency(self.backend_api)

    def shared_api_gateway(self):

        self.api_gateway = SharedApiGateway(
            self.app,
            self.stage,
            self.backend_api.lambda_users_handler,
            self.backend_api.lambda_visits_handler,
            self.backend_api.lambda_qualifications_handler,
            self.backend_api.lambda_equipment_handler,
            self.backend_api.lambda_tiger_training_handler,
            env=self.env, zones=self.dns, create_dns=self.create_dns
        )

        # Dependency ensures this is completely configured prior
        # to continuing on
        self.add_dependency(self.api_gateway)

    def hosted_zones_stack(self):

        self.dns = MakerspaceDns(self.app, self.stage, env=self.env)

        # Dependency ensures this is completely configured prior
        # to continuing on
        self.add_dependency(self.dns)

    def dns_records_stack(self):

        # Can only have cross-stack references in the same environment
        # There is probably a way around this with custom resources, but
        # for now we'll just use unique dns records for beta.
        #
        # See the Domains class where we note that we could use NS records
        # to share sub-domain space.
        self.dns_records = MakerspaceDnsRecords(
            self.app,
            self.stage,
            env=self.env,
            zones=self.dns,
            api_gateway=self.api_gateway.api,
            visit_distribution=self.visit.distribution
        )

        # Dependency ensures this is completely configured prior
        # to continuing on
        self.add_dependency(self.dns_records)

    def cognito_setup(self):

        self.cognito = CognitoConstruct(
            self,
            "MakerspaceCognito",
            user_pool_name="MakerspaceAuth"
        )
