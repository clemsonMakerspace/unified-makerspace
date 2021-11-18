import json


def handler(request, context):

    return {
        'statusCode': 200,
        'body': json.dumps({})
    }