"""
Enables MakerSpace visitors make requests to the staff
regarding equipment.

Warnings: This functionality has not been introduced yet.
"""


import models


def create_request(auth_token: str, request: models.Request):
    """
    Creates a maintenance request.

    ================   ============
    **Endpoint**        /api/requests
    **Request Type**    PUT
    **Access**          ALL
    ================   ============

    Parameters
    ----------
    auth_token : str, required
        Token to verify user credentials.
    request: models.Request
        The request to be made.

    Returns
    -------
    #todo
    request_id: str
    """


def resolve_request(auth_token: str, request_id: str):
    """
    Resolves a request with the given *request_id*.

    ================   ============
    **Endpoint**        /api/requests
    **Request Type**    DELETE
    **Access**          MANAGER
    ================   ============

    Parameters
    ----------
    auth_token : str, required
        Token to verify user credentials.
    request_id: str, required
        The id of the request to be deleted.

    Notes
    -----
    This does **not** delete the request. Resolved requests
    are still stored in the database.

    Returns
    --------
    #todo
    """


def get_requests(auth_token: str):
    """
    Gets all the currently active maintenance requests.

    ================   ============
    **Endpoint**        /api/requests
    **Request Type**    GET
    **Access**          MANAGER
    ================   ============

    Parameters
    ----------
    auth_token : str, required
        Token to verify user credentials.

    Returns
    -------

    """
