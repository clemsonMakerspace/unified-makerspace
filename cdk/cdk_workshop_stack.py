from constructs import Construct

from visit import Visit
from api_gateway import SharedApiGateway
from database import Database
from dns import (MakerspaceDnsRecords, MakerspaceDns, Domains)
from aws_cdk import (
    aws_lambda,
    aws_apigateway as apigw,
    aws_dynamodb as ddb,
)
from aws_cdk import (
    CfnOutput,
)
from aws_cdk import App, Stack, Stage, Environment
from constructs import Construct
from hitcounter import HitCounter
# from cdk_workshop_stack import CdkWorkshopStack
from cdk_dynamo_table_view import TableViewer


class MakerspaceStage(Stage):
    @property
    def hc_endpoint(self):
        return self._hc_endpoint

    @property
    def hc_viewer_url(self):
        return self._hc_viewer_url

    def __init__(self, scope: Construct, stage: str, *,
                 env: Environment) -> None:
        super().__init__(scope, stage, env=env)

        self.service = MakerspaceStack(self, stage, env=env)
        self._hc_endpoint = self.service._hc_endpoint
        self._hc_viewer_url = self.service._hc_viewer_url


class MakerspaceStack(Stack):
    def __init__(self, app: Construct, stage: str, *,
                 env: Environment):
        super().__init__(
            app,
            f'MakerspaceStack-{stage}',
            env=env,
            termination_protection=True)
        self.my_lambda = None
        self.hello_with_counter = None
        self.gateway = None
        self.tv = None
        self._hc_endpoint = None
        self.hc_viewer_url = None

        self.app = app
        self.stage = stage
        self.env = env

        self.domains = Domains(self.stage)

        self.dns = MakerspaceDns(self.app, self.stage, env=self.env)

        self.add_dependency(self.dns)

        self.create_dns = 'dev' not in self.domains.stage

        self.database = Database(self.app, self.stage, env=self.env)

        self.add_dependency(self.database)

        self.visit = Visit(
            self.app,
            self.stage,
            self.database.old_table.table_name,
            self.database.users_table.table_name,
            self.database.visits_table.table_name,
            create_dns=self.create_dns,
            zones=self.dns,
            env=self.env)

        self.add_dependency(self.visit)

        self.database.old_table.grant_read_write_data(
            self.visit.lambda_visit)
        self.database.old_table.grant_write_data(
            self.visit.lambda_register)

        self.database.visits_table.grant_read_write_data(
            self.visit.lambda_visit)

        self.database.users_table.grant_read_data(self.visit.lambda_visit)
        self.database.users_table.grant_read_write_data(
            self.visit.lambda_register)

        self.api_gateway = SharedApiGateway(
            self.app, self.stage, self.visit.lambda_visit, self.visit.lambda_register, env=self.env, zones=self.dns,
            create_dns=self.create_dns)

        self.add_dependency(self.api_gateway)

        # my_lambda
        self.my_lambda = self.visit.lambda_register
        # self.my_lambda = aws_lambda.Function(
        #     self, 'HelloHandler',
        #     runtime=aws_lambda.Runtime.PYTHON_3_7,
        #     code=aws_lambda.Code.from_asset('lambda'),
        #     handler='hello.handler',
        # )

        gateway = self.api_gateway.get_api()

        hello_with_counter = HitCounter(
            self, 'HelloHitCounter',
            downstream=self.my_lambda
        )

        tv = TableViewer(
            self, 'ViewHitCounter',
            title='Hello Hits',
            table=hello_with_counter.table
        )

        self._hc_endpoint = CfnOutput(
            self, 'GatewayUrl',
            value=gateway.url
        )

        self._hc_viewer_url = CfnOutput(
            self, 'TableViewerUrl',
            value=tv.endpoint
        )

    # def database_stack(self):
    #
    #     self.database = Database(self.app, self.stage, env=self.env)
    #
    #     self.add_dependency(self.database)
    #
    # def visitors_stack(self):
    #
    #     self.visit = Visit(
    #         self.app,
    #         self.stage,
    #         self.database.old_table.table_name,
    #         self.database.users_table.table_name,
    #         self.database.visits_table.table_name,
    #         create_dns=self.create_dns,
    #         zones=self.dns,
    #         env=self.env)
    #
    #     self.add_dependency(self.visit)
    #
    # def shared_api_gateway(self):
    #
    #     self.api_gateway = SharedApiGateway(
    #         self.app, self.stage, self.visit.lambda_visit, self.visit.lambda_register, env=self.env, zones=self.dns, create_dns=self.create_dns)
    #
    #     self.add_dependency(self.api_gateway)
    #
    #     # my_lambda
    #     self.my_lambda = self.visit.lambda_register
    #
    #     #gateway
    #     self.gateway = self.api_gateway.api
    #
    #
    # def hosted_zones_stack(self):
    #
    #     self.dns = MakerspaceDns(self.app, self.stage, env=self.env)
    #
    #     self.add_dependency(self.dns)

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

# class CdkWorkshopStack(Stack):

    # def __init__(self, scope: Construct, id: str, **kwargs) -> None:
    #     super().__init__(scope, id, **kwargs)
    #     test_stage = MakerspaceStage(self, 'Dev', env=accounts['Dev-ltn'])
    #     service = test_stage.service
    #     # my_lambda = service.my_lambda
    #     # gateway = service.api_gateway.get_api()
    #
    #
    #     my_lambda = aws_lambda.Function(
    #         self, 'HelloHandler',
    #         runtime=aws_lambda.Runtime.PYTHON_3_7,
    #         code=aws_lambda.Code.from_asset('lambda'),
    #         handler='hello.handler',
    #     )
    #     hello_with_counter = HitCounter(
    #         self, 'HelloHitCounter',
    #         downstream=my_lambda
    #     )
    #     gateway = apigw.LambdaRestApi(
    #         self, 'Endpoint',
    #         handler=hello_with_counter._handler
    #     )
    #
    #     tv = TableViewer(
    #         self, 'ViewHitCounter',
    #         title='Hello Hits',
    #         table=hello_with_counter.table
    #     )
    #
    #     self._hc_endpoint = CfnOutput(
    #         self, 'GatewayUrl',
    #         value=gateway.url
    #     )
    #
    #     self._hc_viewer_url = CfnOutput(
    #         self, 'TableViewerUrl',
    #         value=tv.endpoint
    #     )
