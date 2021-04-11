

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



def reset_password(email: str):
    """
    Sends a password reset email.

    ================   ============
    **Endpoint**        /api/admin
    **Request Type**    PATCH
    **Access**          ANY
    ================   ============

    Parameters
    ----------
    email: str, required
        The email of the user to reset the
        password for.

    Returns
    -------
    Success
    code : int
        Return code.
    message: str

    """
