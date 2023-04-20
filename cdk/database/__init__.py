
from aws_cdk import Stack, Environment, RemovalPolicy, aws_dynamodb
from constructs import Construct


class Database(Stack):
    def __init__(self, scope: Construct,
                 stage: str, *, env: Environment):

        # todo: remove the stage out of the id string, cloudformation already prefixes all dependancies with the stack that its part of and that contains the stack stage
        self.id = f'Database-{stage}'
        self.users_id = f'Database-users-{stage}'
        self.old_visits_id = f'Database-visits-{stage}' #! remove in next pr
        self.visits_id = 'visits'
        
        super().__init__(
            scope, self.id, env=env, termination_protection=True)

        self.dynamodb_old_table()  # This is the original table
        self.dynamodb_visits_table()
        self.dynamodb_users_table()

    def dynamodb_old_table(self):
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

        self.old_table = aws_dynamodb.Table(self,
                                                 self.id,
                                                 point_in_time_recovery=True,
                                                 removal_policy=RemovalPolicy.RETAIN,
                                                 sort_key=aws_dynamodb.Attribute(
                                                     name='SK',
                                                     type=aws_dynamodb.AttributeType.STRING),
                                                 partition_key=aws_dynamodb.Attribute(
                                                     name='PK',
                                                     type=aws_dynamodb.AttributeType.STRING),
                                                 billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST,
                                                 time_to_live_attribute="last_updated")

    def dynamodb_visits_table(self):

        #! remove in next pr
        self.old_visits_table = aws_dynamodb.Table(self,
                                               self.old_visits_id,
                                               point_in_time_recovery=True,
                                               removal_policy=RemovalPolicy.RETAIN,
                                               partition_key=aws_dynamodb.Attribute(
                                                   name='username',
                                                   type=aws_dynamodb.AttributeType.STRING),
                                               sort_key=aws_dynamodb.Attribute(
                                                   name='visit_time',
                                                   type=aws_dynamodb.AttributeType.STRING),
                                                billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST,
                                                time_to_live_attribute="last_updated")
       
        #! remove in next pr
        self.export_value(self.old_visits_table.table_name)
        self.export_value(self.old_visits_table.table_arn)


        self.visits_table = aws_dynamodb.Table(self,
                                               self.visits_id,
                                               point_in_time_recovery=True,
                                               removal_policy=RemovalPolicy.RETAIN,
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
                                              removal_policy=RemovalPolicy.RETAIN,
                                              partition_key=aws_dynamodb.Attribute(
                                                  name='username',
                                                  type=aws_dynamodb.AttributeType.STRING),
                                              billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST,
                                              time_to_live_attribute="last_updated")
