
from aws_cdk import core
from visit import Visit
from api_gateway import SharedApiGateway
from database import Database


class MakerspaceStage(core.Stage):
    def __init__(self, scope: core.Construct, stage: str, **kwargs) -> None:
        super().__init__(scope, stage, **kwargs)

        self.service = MakerspaceStack(self, stage, **kwargs)


class MakerspaceStack(core.Stack):

    def __init__(self, app: core.Construct, stage: str, **kwargs):
        super().__init__(app, f'MakerspaceStack-{stage}', **kwargs)

        self.app = app
        self.stage = stage
        self.env = kwargs['env']

        self.database_stack()

        self.visitors_stack()

        self.shared_api_gateway()

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

    def shared_api_gateway(self):

        self.api_gateway = SharedApiGateway(
            self.app, self.stage, self.visit.lambda_, env=self.env)

        self.add_dependency(self.api_gateway)
