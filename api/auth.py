import requests
import models
import json

def create_user(email: str, password: str):
    """
    Creates a new user in the Cognito Pool.
    ================   ============
    **Endpoint**        /api/users
    **Request Type**    POST
    **Access**          ALL
    ================   ============
    Parameters
    -----------
    email : str, required
        The email of the user.
    password : str, required
        The raw password of the user.
    Returns
    --------
    UserCreationSuccess
    code: int
        Return Code
    message: str
        Response Message
    auth_token: str
        The authentication token of the newly created user.
    EmailInUse
    code: int
        Return Code
    message: str
        Response Message
    """

    payload = {'username':email,'password':password,'email':email, 'first': 'my', 'last': 'name'}
    response = requests.put("https://muq6dxolc9.execute-api.us-east-1.amazonaws.com/prod/CreateUser", data = json.dumps(payload))

    return response.json()

def delete_user(auth_token: str, user_id: str):
    """
    Deletes a user specified by their email.
    ================   ============
    **Endpoint**        /api/users
    **Request Type**    DELETE
    **Access**          MANAGER
    ================   ============
    Parameters
    -----------
    auth_token : str, required
        Token to verify user credentials.
    user_id : str, required
        The id of the user.
    Returns
    --------
    Success
    code: int
        Return Code
    message: str
        Response Message
    InsufficientPermissions
    code: int
        Return Code
    message: str
        Response Message
    """
    payload = {'username':user_id, 'auth_token':auth_token}
    response = requests.delete("https://6reu9k3vt9.execute-api.us-east-1.amazonaws.com/prod/RemoveUser", data = json.dumps(payload))
    
    return response.json()

def get_users(auth_token: str):
    """
    Gets all the users with their permissions.
    ================   ============
    **Endpoint**        /api/users
    **Request Type**    GET
    **Access**          MANAGER
    ================   ============
    Parameters
    -----------
    auth_token : str, required
        Token to verify user credentials.
    Returns
    --------
    Success
    code: int
        Return Code
    users: [models.User]
        List of returned users.
    """


def update_permissions(auth_token: str, user_id: str, user: models.User):
    """
    Gets all the users with their permissions.
    ================   ============
    **Endpoint**        /api/users
    **Request Type**    PATCH
    **Access**          MANAGER
    ================   ============
    Parameters
    -----------
    auth_token : str, required
        Token to verify user credentials.
    user_id: str, required
        The id of the user to update permissions for.
    user:
        The new user object with changed permissions.
    Returns
    --------
    Success
    code: int
        Return Code
    """