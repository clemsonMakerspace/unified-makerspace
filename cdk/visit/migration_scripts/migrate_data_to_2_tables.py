"""
This script will migrate data from the original table to the two
new tables.
"""
from typing import Tuple, List
import boto3
import os
import datetime


def generate_role_arn() -> str:
    """
    Generate a role arn for the migration script.

    Returns:
        A role arn.
    """
    return 'arn:aws:iam::{}:role/{}'.format(os.environ['AWS_ACCOUNT_ID'], 'data_migration_role')


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


def process_grad_date(grad_date: str) -> Tuple[str, int]:
    """
    Infers the graduation semester and year from grad_date

    grad_date: str
        The graduation date in the format 'YYYY-MM-DD'

    Returns:
        A tuple of the semester and year.
    """
    year = grad_date[:4]
    month = grad_date[5:7]
    if month in ['04', '05', '06']:
        semester = 'Spring'
    elif month in ['07', '08', '09']:
        semester = 'Summer'
    elif month in ['11', '12', '01']:
        semester = 'Fall'
    else:
        semester = "None"

    return semester, int(year)


def process_timestamp(timestamp: str) -> str:
    """
    Convert timestamp from ISO Format to Seconds Since Epoch
    Example: 2022-04-11 03:14:50.800970
    """
    return str(datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f").timestamp())


def get_cleaned_majors_or_minors(major_or_minor: str) -> List[str]:
    """
    Cleans the major or minor string.

    Args:
        major_or_minor: The major or minor string to clean.

    Returns:
        A cleaned major or minor string.
    """
    if major_or_minor is None or len(major_or_minor) == 0:
        return []

    print(major_or_minor)

    if major_or_minor[0] == '[':
        major_or_minor = major_or_minor[1:-1]
        list_of_vals = [val.split(":")[1][1:-2]
                        for val in major_or_minor.split(',')]
        return list_of_vals
    else:
        return major_or_minor.split(',')


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

    visits = []
    users = []

    dynamodbclient = boto3.client('dynamodb', region_name='us-east-1')
    # Iterate over the table. If PK is a timestamp, this is a visit
    for row in original_data:
        if row['PK'][0].isdigit():
            location = row['location'] if 'location' in row else 'watt'
            visits.append(
                {'visit_time': {'S': row['PK']}, 'username': {'S': row['SK'].lower()}, 'location': {'S': location}})
        else:
            grad_semester, grad_year = process_grad_date(row['Grad_date'])
            majors = get_cleaned_majors_or_minors(
                row['Major']) if 'Major' in row else ["a", "b"]

            minors = get_cleaned_majors_or_minors(
                row['Minor']) if 'Minor' in row else ["a", "b"]

            updated_registration_time = process_timestamp(row['SK'])

            users.append({'username': {'S': row['PK'].lower()},
                          'register_time': {'N': updated_registration_time},
                          'date_of_birth': {'S': row['DOB']},
                          'first_name': {'S': row['firstName']},
                          'gender': {'S': row['Gender']},
                          'grad_semester': {'S': grad_semester},
                          'grad_year': {'S': str(grad_year)},
                          'last_name': {'S': row['lastName']},
                          'major': {'L': [{'S': major} for major in majors]},
                          'minor': {'L': [{'S': minor} for minor in minors]}})

    for visit in visits:
        dynamodbclient.put_item(Item=visit, TableName=visits_table_name)

    for user in users:
        print(user)
        dynamodbclient.put_item(Item=user, TableName=users_table_name)

    print("Migration Done! :-)")
