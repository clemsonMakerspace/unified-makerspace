"""
Checks to see if an api key matching a provided name already
exists in the environment. If it does, it returns the id of
the key, if it does not, it returns an empty string for the id.

Expected input:
{ 'ApiKeyName': <NAME_OF_API_KEY> }

Output:
{ 'Data': {'ApiKeyId': <ID>} }
"""

import boto3
import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):

    logger.info("Event:")
    logger.info(json.dumps(event, indent=2))
    
    try:
        client = boto3.client('apigateway')

        if 'ApiKeyName' not in event:
            raise Exception("Missing 'ApiKeyName' from event input fields.")

        api_key_name = event['ApiKeyName']

        response = client.get_api_keys(includeValues=False)
        key_data = None

        for key in response['items']:
            if key['name'] == api_key_name:
                key_data = {'Data': {'ApiKeyId': key['id']}}
                break

        if not key_data:
            key_data = {'Data': {'ApiKeyId': ""}}

        logger.info("Key data")
        logger.info(json.dumps(key_data, indent=2))

        return key_data

    except Exception as e:
        raise Exception(f"Error retrieving API Key: {e}")
