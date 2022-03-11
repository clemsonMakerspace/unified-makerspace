
from aws_cdk import (
    core,
    aws_dynamodb
)


class Database(core.Stack):
    def __init__(self, scope: core.Construct,
                 stage: str, *, env: core.Environment):
        self.id = f'Database-{stage}'
        super().__init__(scope, self.id, env=env, termination_protection=True)

        self.dynamodb_dual_tables()

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

        self.table = aws_dynamodb.Table(self,
                                        self.id,
                                        point_in_time_recovery=True,
                                        removal_policy=core.RemovalPolicy.RETAIN,
                                        sort_key=aws_dynamodb.Attribute(
                                            name='SK',
                                            type=aws_dynamodb.AttributeType.STRING),
                                        partition_key=aws_dynamodb.Attribute(
                                            name='PK',
                                            type=aws_dynamodb.AttributeType.STRING))

    def dynamodb_dual_tables(self):
        """
        This table design has us use multiple dyanmoDB tables for tracking
        the visits and the users. Ideally, by separating the two, we can more
        easily perform data analytics.

        Visits:

        - PK = `{date}`
        - SK = `{username}`

        Visitors:

        - PK = username
        - SK = `VISITOR_INFORMATION`
        """
        # TODO: This fails on an ID error. What is self.id? Do we need to make
        # 2 stacks for the database? This just seems a little redundant.
        self.visits_table = aws_dynamodb.Table(self,
                                               self.id,
                                               point_in_time_recovery=True,
                                               removal_policy=core.RemovalPolicy.RETAIN,
                                               sort_key=aws_dynamodb.Attribute(
                                                   name='SK',
                                                   type=aws_dynamodb.AttributeType.STRING),
                                               partition_key=aws_dynamodb.Attribute(
                                                   name='PK',
                                                   type=aws_dynamodb.AttributeType.NUMBER))

        self.users_table = aws_dynamodb.Table(self,
                                              self.id,
                                              point_in_time_recovery=True,
                                              removal_policy=core.RemovalPolicy.RETAIN,
                                              sort_key=aws_dynamodb.Attribute(
                                                  name='SK',
                                                  type=aws_dynamodb.AttributeType.STRING),
                                              partition_key=aws_dynamodb.Attribute(
                                                  name='PK',
                                                  type=aws_dynamodb.AttributeType.STRING))
