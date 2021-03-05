import models


def create_request(auth_token: str, request: models.Request):
    """
    Creates a maintenance request for the MakerSpace.

    ================   ============
    **Endpoint**        /api/requests/create
    **Request Type**    POST
    **Access**          ALL
    ================   ============

    Parameters
    ----------
    auth_token
    request: models.Request

    Returns
    -------
    request_id: str
    """


def delete_request(auth_token: str, request_id: str):
    """
    ================   ============
    **Endpoint**        /api/requests/create
    **Request Type**    POST
    **Access**          ALL
    ================   ============

    Parameters
    ----------
    auth_token
    request_id

    Returns
    --------



def get_requests(auth_token: str):
    """
    == == == == == == == == == == == == == ==
    ** Endpoint ** / api / requests / create
    ** Request
    Type ** POST
    ** Access ** MANAGERS
    == == == == == == == == == == == == == ==

    Parameters
    ----------
    auth_token
    name: str
    message: str

    Returns
    -------

    """
