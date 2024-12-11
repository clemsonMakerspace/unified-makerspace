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
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def delete_key(client, api_key_name: str) -> bool:
    """
    Tries to delete a key by name.

    :params client: An apigateway client.
    :params api_key_name: The name of the key to delete.
    :returns: True if a key was deleted, False otherwise.
    """

    deleted_key: bool = False

    response = client.get_api_keys(includeValues=False)

    # Check for matching key name
    for key in response['items']:
        if key['name'] == api_key_name:

            # Delete the key
            try:
                client.delete_api_key(apiKey=key['id'])
                logger.info(f"Deleted key '{key['id']}'")
                deleted_key = True
            except Exception as e:
                raise Exception(f"Error deleting API Key: {e}")

    return deleted_key

def handler(event, context):

    logger.info("Event:")
    logger.info(json.dumps(event, indent=2))
    
    try:
        client = boto3.client('apigateway')

        if 'ApiKeyName' not in event:
            raise Exception("Missing 'ApiKeyName' from event input fields.")

        api_key_name = event['ApiKeyName']

        # Try and delete the key
        delete_key(client, api_key_name)

        # Wait 5 seconds for changes to propagate
        time.sleep(5)

        # Ensure key was deleted (delete_key should return False for no key deleted)
        key_deleted: bool = delete_key(client, api_key_name)

        if key_deleted:
            raise Exception(f"Api key still existed after deleting first time.")

        return {}

    except Exception as e:
        raise Exception(f"Error occurred: {e}")
