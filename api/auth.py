def create_user(email: str, password: str, role: str):
    """
    Creates a new user in the Cognito Pool.

    Parameters
    -----------
    email : str
        The email of the user.
    password : str
        The raw password of the user.
    role : str
        Specified role of the user.

    Returns
    --------
    code
        200
    token : str
       32-bit authentication token.


    Raises
    -------
    code
        400
    message: str
        The email is already in use.
    """


def delete_user(email: str, auth_token: str):
    """
    Deletes a user specified by their email.

    Parameters
    -----------
    email : str
        The email of the user.
    auth_token : str
        Token to very user credentials.

    Returns
    --------
    code
       200
    message
       The user has been successfully deleted.

    """
