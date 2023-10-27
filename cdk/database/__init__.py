
from aws_cdk import (
    core,
    aws_dynamodb
)


class Database(core.Stack):
    def __init__(self, scope: core.Construct,
                 stage: str, *, env: core.Environment):

        # todo: remove the stage out of the id string, cloudformation already prefixes all dependancies with the stack that its part of and that contains the stack stage
        self.id = f'Database-{stage}'
        self.users_id = 'users'
        self.visits_id = 'visits'

        super().__init__(
            scope, self.id, env=env, termination_protection=True)

        self.dynamodb_visits_table()
        self.dynamodb_users_table()

    def dynamodb_visits_table(self):
        self.visits_table = aws_dynamodb.Table(self,
                                               self.visits_id,
                                               point_in_time_recovery=True,
                                               removal_policy=core.RemovalPolicy.RETAIN,
                                               partition_key=aws_dynamodb.Attribute(
                                                   name='username',
                                                   type=aws_dynamodb.AttributeType.STRING),
                                               sort_key=aws_dynamodb.Attribute(
                                                   name='visit_time',
                                                   type=aws_dynamodb.AttributeType.NUMBER),
                                               billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST,
                                               time_to_live_attribute="last_updated")

    def dynamodb_users_table(self):
        self.users_table = aws_dynamodb.Table(self,
                                              self.users_id,
                                              point_in_time_recovery=True,
                                              removal_policy=core.RemovalPolicy.RETAIN,
                                              partition_key=aws_dynamodb.Attribute(
                                                  name='username',
                                                  type=aws_dynamodb.AttributeType.STRING),
                                              billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST,
                                              time_to_live_attribute="last_updated")
