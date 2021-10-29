
from aws_cdk import core
from visit import Visit
from api_gateway import SharedApiGateway
from database import Database
from dns import (MakerspaceDnsRecords, MakerspaceDns, Domains)


class MakerspaceStage(core.Stage):
    def __init__(self, scope: core.Construct, stage: str, *,
                 env: core.Environment) -> None:
        super().__init__(scope, stage, env=env)

        self.domains = Domains(stage)

        self.dns = MakerspaceDns(self, stage, env=env)

        self.service = MakerspaceStack(
            self, stage, env=env, domains=self.domains)

        # Can only have cross-stack references in the same environment
        # There is probably a way around this with custom resources, but
        # for now we'll just not have any beta DNS records
        self.dns_records = MakerspaceDnsRecords(self, stage,
                                                env=env,
                                                zones=self.dns,
                                                api_gateway=self.service.api_gateway.api,
                                                visit_distribution=self.service.visit.distribution)


class MakerspaceStack(core.Stack):

    def __init__(self, app: core.Construct, stage: str, *,
                 env: core.Environment, domains: Domains):
        super().__init__(app, f'MakerspaceStack-{stage}', env=env)

        self.app = app
        self.stage = stage
        self.env = env

        self.database_stack()

        self.visitors_stack()

        self.shared_api_gateway(domains)

    def database_stack(self):

        self.database = Database(self.app, self.stage, env=self.env)

        self.add_dependency(self.database)

    def visitors_stack(self):

        self.visit = Visit(
            self.app,
            self.stage,
            self.database.table.table_name,
            env=self.env)

        self.add_dependency(self.visit)

    def shared_api_gateway(self, domains: Domains):

        self.api_gateway = SharedApiGateway(
            self.app, self.stage, self.visit.lambda_, env=self.env, domains=domains)

        self.add_dependency(self.api_gateway)
