import logging
from aws_cdk import (
    core,
    aws_dynamodb
)


class Database(core.Stack):
    def __init__(self, scope: core.Construct,
                 stage: str, *, env: core.Environment):
        # Sets up CloudWatch logs and sets level to INFO
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        self.id = 'Database'        
        self.users_id = 'users'
        self.visits_id = 'visits'
        self.equipment_id = 'equipment'
        self.qualifications_id = 'qualifications'

        super().__init__(
            scope, self.id, env=env, termination_protection=True)
        
        self.dynamodb_users_table()
        self.dynamodb_visits_table()
        self.dynamodb_equipment_table()
        self.dynamodb_qualifications_table()

    def dynamodb_users_table(self):
        """
        Description:
            Creates the users database table variable

        Users:
            - PK = `{user_id}` : string

        Example Query:
            Query the DynamoDB table by `user_id` as the partition key.

            Pseudocode:
            dynamodb.query({
                KeyConditionExpression: Key('user_id').eq('{user_id_value}')
            })
        """
                
        self.users_table = aws_dynamodb.Table(self,
                                              self.users_id,
                                              point_in_time_recovery=True,
                                              removal_policy=core.RemovalPolicy.RETAIN,
                                              partition_key=aws_dynamodb.Attribute(
                                                  name='user_id',
                                                  type=aws_dynamodb.AttributeType.STRING),
                                              billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST)
        

    def dynamodb_visits_table(self):
        """
        Description:
            Creates the visits database table variable
            Adds the GSI to the visits_table

        Visits:
            - PK = `{user_id}` : string
            - SK = `{timestamp}` : string

        GSI (TimestampIndex):
            - PK = `{_ignore}` : string
            - SK = `{timestamp}` : string

        Example Query:
            python-pseudocode
                Query the visits table by `user_id` and `timestamp`:
                    dynamodb.query({
                        KeyConditionExpression: Key('user_id').eq('{user_id_value}') 
                                                & Key('timestamp').eq('{timestamp_value}')
                    })
            
                Query the TimestampIndex by `_ignore` and `timestamp`:
                    dynamodb.query({
                        IndexName: 'TimestampIndex',
                        KeyConditionExpression: Key('_ignore').eq('{ignore_value}') & 
                                                Key('timestamp').eq('{timestamp_value}')
                    })
        """
        
        self.visits_table = aws_dynamodb.Table(self,
                                                self.visits_id,
                                                point_in_time_recovery=True,
                                                removal_policy=core.RemovalPolicy.RETAIN,
                                                sort_key=aws_dynamodb.Attribute(
                                                    name='user_id',
                                                    type=aws_dynamodb.AttributeType.STRING),
                                                partition_key=aws_dynamodb.Attribute(
                                                    name='timestamp',
                                                    type=aws_dynamodb.AttributeType.STRING),
                                                billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST)
        
        # Add GSI with _ignore as partition key and timestamp as sort key
        self.visits_table.add_global_secondary_index(
            index_name="TimestampIndex",
            partition_key=aws_dynamodb.Attribute(
                name='_ignore',
                type=aws_dynamodb.AttributeType.STRING),
            sort_key=aws_dynamodb.Attribute(
                name='timestamp',
                type=aws_dynamodb.AttributeType.STRING)
        )

    def dynamodb_equipment_table(self):
        """
        Description:
            Creates the equipment database table variable
            Adds the GSI to the equipment_table

        Equipment:
            - PK = `{user_id}` : string
            - SK = `{timestamp}` : string

        GSI (TimestampIndex):
            - PK = `{_ignore}` : string
            - SK = `{timestamp}` : string

        Example Query:
            python-pseudocode
                Query the equipment table by `user_id` and `timestamp`:
                    dynamodb.query({
                        KeyConditionExpression: Key('user_id').eq('{user_id_value}') 
                                                & Key('timestamp').eq('{timestamp_value}')
                    })
            
                Query the TimestampIndex by `_ignore` and `timestamp`:
                    dynamodb.query({
                        IndexName: 'TimestampIndex',
                        KeyConditionExpression: Key('_ignore').eq('{ignore_value}') & 
                                                Key('timestamp').eq('{timestamp_value}')
                    })
        """
        
        self.equipment_table = aws_dynamodb.Table(self,
                                                self.equipment_id,
                                                point_in_time_recovery=True,
                                                removal_policy=core.RemovalPolicy.RETAIN,
                                                sort_key=aws_dynamodb.Attribute(
                                                    name='user_id',
                                                    type=aws_dynamodb.AttributeType.STRING),
                                                partition_key=aws_dynamodb.Attribute(
                                                    name='timestamp',
                                                    type=aws_dynamodb.AttributeType.STRING),
                                                billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST)
        
        # Add GSI with _ignore as partition key and timestamp as sort key
        self.equipment_table.add_global_secondary_index(
            index_name="TimestampIndex",
            partition_key=aws_dynamodb.Attribute(
                name='_ignore',
                type=aws_dynamodb.AttributeType.STRING),
            sort_key=aws_dynamodb.Attribute(
                name='timestamp',
                type=aws_dynamodb.AttributeType.STRING)
        )

    def dynamodb_qualifications_table(self):
        """
        Description:
            Creates the qualifications database table variable
            Adds the GSI to the qualifications_table

        Visits:
            - PK = `{user_id}` : string
            - SK = `{last_updated}` : string

        GSI (TimestampIndex):
            - PK = `{_ignore}` : string
            - SK = `{last_updated}` : string

        Example Query:
            python-pseudocode
                Query the qualifications table by `user_id` and `last_updated`:
                    dynamodb.query({
                        KeyConditionExpression: Key('user_id').eq('{user_id_value}') 
                                                & Key('last_updated').eq('{last_updated_value}')
                    })
            
                Query the TimestampIndex by `_ignore` and `last_updated`:
                    dynamodb.query({
                        IndexName: 'TimestampIndex',
                        KeyConditionExpression: Key('_ignore').eq('{ignore_value}') & 
                                                Key('last_updated').eq('{last_updated_value}')
                    })
        """
        
        self.qualifications_table = aws_dynamodb.Table(self,
                                                self.qualifications_id,
                                                point_in_time_recovery=True,
                                                removal_policy=core.RemovalPolicy.RETAIN,
                                                sort_key=aws_dynamodb.Attribute(
                                                    name='user_id',
                                                    type=aws_dynamodb.AttributeType.STRING),
                                                partition_key=aws_dynamodb.Attribute(
                                                    name='last_updated',
                                                    type=aws_dynamodb.AttributeType.STRING),
                                                billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST)
        
        # Add GSI with _ignore as partition key and last_updated as sort key
        self.qualifications_table.add_global_secondary_index(
            index_name="TimestampIndex",
            partition_key=aws_dynamodb.Attribute(
                name='_ignore',
                type=aws_dynamodb.AttributeType.STRING),
            sort_key=aws_dynamodb.Attribute(
                name='last_updated',
                type=aws_dynamodb.AttributeType.STRING)
        )