
from aws_cdk import (
    core,
    aws_dynamodb
)


class Database(core.Stack):
    def __init__(self, scope: core.Construct,
                 stage: str, *, env: core.Environment):
        self.id = f'Database-{stage}'
        self.users_id = f'Database-users-{stage}'
        self.visits_id = f'Database-visits-{stage}'
        self.new_visits_id = 'visits'

        super().__init__(
            scope, self.id, env=env, termination_protection=True)

        self.dynamodb_single_table()  # This is the original table
        self.dynamodb_visits_table()
        self.dynamodb_users_table()

    def dynamodb_single_table(self):
        """
        A single-table design DynamoDB table for all makerspace data.

        This table uses the PK/SK key layout described by Rick Houlihan in his
        DynamoDB talks[1]. This allows us to be flexible moving forward adding
        new features. It's not ideal for analytics, but we can address that
        problem when we get there.

        For now, the following data types can be supported with the described
        schemas:

        Visits:

        - PK = `{date}`
        - SK = `{username}`

        Visitors:

        - PK = `CLEMSON_STUDENT#{clemson-username}`
        - SK = `VISITOR_INFORMATION`

        - PK = `NON_STUDENT_VISITOR#{full-email-address}`
        - SK = `VISITOR_INFORMATION`

        ```python-pseudocode
        dynamodb.get_item({
            PartitionKey={
                'PK': 'CLEMSON_STUDENT#mhall6'
            },
            SortKey={
                'SK': 'VISITOR_INFORMATION'
            }
        })
        ```

        [1]: https://www.youtube.com/watch?v=KYy8X8t4MB8
        """

        self.original_table = aws_dynamodb.Table(self,
                                                 self.id,
                                                 point_in_time_recovery=True,
                                                 removal_policy=core.RemovalPolicy.RETAIN,
                                                 sort_key=aws_dynamodb.Attribute(
                                                     name='SK',
                                                     type=aws_dynamodb.AttributeType.STRING),
                                                 partition_key=aws_dynamodb.Attribute(
                                                     name='PK',
                                                     type=aws_dynamodb.AttributeType.STRING))

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
                                                   type=aws_dynamodb.AttributeType.STRING))

        #! new table used to swap the type of the sk, as the
        #! visitor stack is dependent on this database stack
        self.new_visits_table = aws_dynamodb.Table(self,
                                               self.new_visits_id,
                                               point_in_time_recovery=True,
                                               removal_policy=core.RemovalPolicy.RETAIN,
                                               partition_key=aws_dynamodb.Attribute(
                                                   name='username',
                                                   type=aws_dynamodb.AttributeType.STRING),
                                               sort_key=aws_dynamodb.Attribute(
                                                   name='visit_time',
                                                   type=aws_dynamodb.AttributeType.NUMBER))

    def dynamodb_users_table(self):
        self.users_table = aws_dynamodb.Table(self,
                                              self.users_id,
                                              point_in_time_recovery=True,
                                              removal_policy=core.RemovalPolicy.RETAIN,
                                              partition_key=aws_dynamodb.Attribute(
                                                  name='username',
                                                  type=aws_dynamodb.AttributeType.STRING))
