"""
Checks to see if an api key matching a provided name already
exists in the environment. If it does, it deletes the key.

Expected input:
{ 'ApiKeyName': <NAME_OF_API_KEY> }

Output:
{}
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

        # Check for matching key name
        for key in response['items']:
            if key['name'] == api_key_name:

                # Delete the key
                try:
                    client.delete_api_key(apiKey=key['id'])
                    logger.info(f"Deleted key '{key['id']}'")
                except Exception as e:
                    raise Exception(f"Error deleting API Key: {e}")

        return {}

    except Exception as e:
        raise Exception(f"Error occurred: {e}")
