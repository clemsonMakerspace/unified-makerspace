

def generate_user_token(auth_token: str):
    """
    Generates a random token to create an
    account for a new user.

    ================   ============
    **Endpoint**        /api/admin
    **Request Type**    POST
    **Access**          MANAGER
    ================   ============

    Parameters
    ----------
    auth_token : str, required
        Token to verify user credentials.

    Returns
    -------
    Success
    code : int
        Return code.
    user_token : str
        N-digit token used to create a user.

    """