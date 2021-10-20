
from aws_cdk import core
from visit import Visit
from api_gateway import SharedApiGateway
from database import Database


class MakerspaceStack:

    def __init__(self, app: core.Construct, stage: str, env: core.Environment):
        self.app = app
        self.stage = stage
        self.env = env

    def synth(self):
        database = Database(self.app, self.stage, env=self.env)
        visit = Visit(
            self.app,
            self.stage,
            database.table.table_name,
            env=self.env)

        SharedApiGateway(self.app, self.stage, visit.lambda_, env=self.env)
