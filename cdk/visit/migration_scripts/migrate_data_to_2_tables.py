"""
This script will migrate data from the original table to the two
new tables.
"""

import boto3
import os


def generate_role_arn() -> str:
    """
    Generate a role arn for the migration script.

    Returns:
        A role arn.
    """
    return 'arn:aws:iam::{}:role/{}'.format(os.environ['AWS_ACCOUNT_ID'], 'migration-role')


def get_table(table_name: str) -> boto3.resources.base.ServiceResource:
    """
    Get a table resource from the boto3 resource manager.

    Args:
        table_name: The name of the table to get.

    Returns:
        A table resource.
    """
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table(table_name)
    return table


def get_all_data(table: boto3.resources.base.ServiceResource) -> list:
    """
    Get all data from a table.

    Args:
        table: The table to get data from.

    Returns:
        A list of all data from the table.
    """
    response = table.scan()
    return response['Items']


# This part runs the migration
if __name__ == '__main__':
    client = boto3.client('sts')
    response = client.assume_role(
        RoleArn=generate_role_arn(),
        RoleSessionName="data_migration_session")

    original_table_name = os.environ["ORIGINAL_TABLE_NAME"]
    visits_table_name = os.environ["VISITS_TABLE_NAME"]
    users_table_name = os.environ["USERS_TABLE_NAME"]

    original_table = get_table(original_table_name)
    visits_table = get_table(visits_table_name)
    users_table = get_table(users_table_name)

    # Get all users from the original_table
    original_data = get_all_data(original_table)

    # Iterate over the table. If PK is a timestamp, this is a visit
    for row in original_data:
        if row['PK'].isdigit():
            if 'location' in row:
                visits_table.put_item(
                    Item={'visit_time': int(row['PK']), 'username': row['SK'], 'location': row['location']})
            else:
                visits_table.put_item(
                    Item={'visit_time': int(row['PK']), 'username': row['SK'], 'location': ''})
        else:
            users_table.put_item(
                Item={'username': row['PK'].lower(), 'register_time': row['SK'],
                      'date_of_birth': row['DOB'], 'first_name': row['firstName'],
                      'gender': row['Gender'], 'grad_date': row['Grad_date'],
                      'last_name': row['lastName'], 'major': row['Major'],
                      'minor': row['Minor']})

    print("Migration Done! :-)")
