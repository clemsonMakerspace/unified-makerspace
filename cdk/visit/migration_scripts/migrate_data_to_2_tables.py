import boto3
import os

original_table_name = os.environ["TABLE_NAME"]
visits_table_name = os.environ["VISITS_TABLE_NAME"]
users_table_name = os.environ["USERS_TABLE_NAME"]


def get_table(table_name: str) -> boto3.resources.base.ServiceResource:
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table(table_name)
    return table


if __name__ == '__main__':
    # TODO: Replace with the actual table names
    original_table = get_table(original_table_name)
    visits_table = get_table(visits_table_name)
    users_table = get_table(users_table_name)

    # TODO: Get all users from the original_table

    # TODO: For each user, get all visits from the original_table

    # TODO: For each visit, insert into visits_table

    # TODO: For each user, insert into users_table
