
import json


def handler(request, context):
    """
    Register the input of a user (namely, the username) from the makerspace console.

    This should:

    1. Check whether this user has visited before by looking for a
       sentinel record in the table
    2. Trigger a registration workflow if this is the first time for that user
    3. Place a visit entry into the table
    """

    return {
        'statusCode': 200,
        'body': json.dumps({})
    }
