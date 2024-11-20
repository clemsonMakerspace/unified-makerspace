
from aws_cdk import core
from visit import Visit
from api_gateway.shared_api_gateway import SharedApiGateway
from api_gateway.backend_api import BackendApi
from database import Database
from dns import (MakerspaceDnsRecords, MakerspaceDns, Domains)
from cognito.cognito_construct import CognitoConstruct
# from data_migration import DataMigrationStack

class MakerspaceStage(core.Stage):
    def __init__(self, scope: core.Construct, stage: str, *,
                 env: core.Environment) -> None:
        super().__init__(scope, stage, env=env)
        
        self.service = MakerspaceStack(self, stage, env=env)


class MakerspaceStack(core.Stack):

    def __init__(self, app: core.Construct, stage: str, *,
                 env: core.Environment):
        super().__init__(
            app,
            'MakerspaceStack',
            env=env,
            termination_protection=True)

        self.app = app
        self.stage = stage
        self.env = env

        self.domains = Domains(self.stage)

        self.hosted_zones_stack()

        self.create_dns = 'dev' not in self.domains.stage

        self.database_stack()

        self.visitors_stack()

        self.backend_stack()

        self.cognito_setup()

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

        self.shared_api_gateway()

        if self.create_dns:
            self.dns_records_stack()
            
        # if self.stage.lower() == 'prod':
        #     self.data_migration_stack()
            
    # def data_migration_stack(self):
        
    #     self.migration = DataMigrationStack(self.app, self.stage, env=self.env)
        
    #     self.add_dependency(self.migration)
        

    def database_stack(self):

        self.database = Database(self.app, self.stage, env=self.env)

        self.add_dependency(self.database)

    def visitors_stack(self):

        self.visit = Visit(
            self.app,
            self.stage,
            create_dns=self.create_dns,
            zones=self.dns,
            env=self.env
        )

        self.add_dependency(self.visit)

    def backend_stack(self):

        self.backend_api = BackendApi(
            self.app,
            self.stage,
            self.database.users_table.table_name,
            self.database.visits_table.table_name,
            self.database.equipment_table.table_name,
            self.database.qualifications_table.table_name,
            zones=self.dns,
            env=self.env
        )

        self.add_dependency(self.backend_api)

    def shared_api_gateway(self):

        self.api_gateway = SharedApiGateway(
            self.app,
            self.stage,
            self.backend_api.lambda_users_handler,
            self.backend_api.lambda_visits_handler,
            self.backend_api.lambda_qualifications_handler,
            self.backend_api.lambda_equipment_handler,
            env=self.env, zones=self.dns, create_dns=self.create_dns
        )

        self.add_dependency(self.api_gateway)

    def hosted_zones_stack(self):

        self.dns = MakerspaceDns(self.app, self.stage, env=self.env)

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

        self.add_dependency(self.dns_records)

    def cognito_setup(self):

        self.cognito = CognitoConstruct(
            self,
            "MakerspaceCognito",
            user_pool_name="MakerspaceAuth"
        )
