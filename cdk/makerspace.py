
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
    def __init__(self, scope: Construct, stage: str, *,
                 env: Environment) -> None:
        super().__init__(scope, stage, env=env)
        
        self.service = MakerspaceStack(self, stage, env=env)


class MakerspaceStack(Stack):

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

        # Get the api key value to use for backend api requests
        secret_name: str = "SharedApiGatewayKey"
        shared_gateway_secret = aws_secretsmanager.Secret.from_secret_name_v2(
                self,
                "SharedGatewaySecret",
                secret_name
        )
        secret_value = SecretValue.secrets_manager(shared_gateway_secret.secret_name)
        self.backend_api_key: str = secret_value.to_string()
        print(f"API KEY: {self.backend_api_key}")
        
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

        self.database.users_table.grant_read_data(self.backend_api.lambda_visits_handler)
        self.database.users_table.grant_read_data(self.backend_api.lambda_equipment_handler)
        self.database.users_table.grant_read_write_data(self.backend_api.lambda_users_handler)
        
        #! Do not have a lambda register handler
        # self.database.users_table.grant_read_write_data(
        #     self.backend_api.lambda_register_handler)
        
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
            backend_api_key=self.backend_api_key,
            backend_api_url=self.api_gateway.url
        )

        # Dependency ensures this is completely configured prior
        # to continuing on
        self.add_dependency(self.visit)

    def backend_stack(self):
        """ 
        Creates the BackendApi Stack in CloudFormation
        Creates and configures all Lambda functions utilized
            by the SharedApiGateway Stack; grants the appropriate
            permissions to the functions to allow the 
        
        """

        if self.create_dns:
            domain_name = self.dns.api_hosted_zone.zone_name
            backend_api_url: str = f"https://{domain_name}"
        else:
            backend_api_url: str = ""

        self.backend_api = BackendApi(
            self.app,
            self.stage,
            self.database.users_table.table_name,
            self.database.visits_table.table_name,
            self.database.equipment_table.table_name,
            self.database.qualifications_table.table_name,
            zones=self.dns,
            env=self.env,
            backend_api_key=self.backend_api_key,
            backend_api_url=backend_api_url
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
            backend_api_key=self.backend_api_key,
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
