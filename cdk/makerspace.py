
from aws_cdk import core
from visit import Visit
from api_gateway import SharedApiGateway
from database import Database
from dns import (MakerspaceDnsRecords, MakerspaceDns, Domains)


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
            f'MakerspaceStack-{stage}',
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

        self.database.original_table.grant_read_write_data(
            self.visit.lambda_visit)
        self.database.original_table.grant_write_data(
            self.visit.lambda_register)

        self.database.visits_table.grant_read_write_data(
            self.visit.lambda_visit)
        self.database.users_table.grant_read_data(self.visit.lambda_visit)
        self.database.users_table.grant_read_write_data(
            self.visit.lambda_register)

        self.shared_api_gateway()

        if self.create_dns:
            self.dns_records_stack()

    def database_stack(self):

        self.database = Database(self.app, self.stage, env=self.env)

        self.add_dependency(self.database)

    def visitors_stack(self):

        self.visit = Visit(
            self.app,
            self.stage,
            self.database.original_table.table_name,
            self.database.users_table.table_name,
            self.database.visits_table.table_name,
            create_dns=self.create_dns,
            zones=self.dns,
            env=self.env)

        self.add_dependency(self.visit)

    def shared_api_gateway(self):

        self.api_gateway = SharedApiGateway(
            self.app, self.stage, self.visit.lambda_visit, self.visit.lambda_register, env=self.env, zones=self.dns, create_dns=self.create_dns)

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
        self.dns_records = MakerspaceDnsRecords(self.app, self.stage,
                                                env=self.env,
                                                zones=self.dns,
                                                api_gateway=self.api_gateway.api,
                                                visit_distribution=self.visit.distribution)

        self.add_dependency(self.dns_records)
