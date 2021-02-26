import flask

app = flask.Flask('__main__')

def get_users():
    pass


@app.route('/users/')
def create_user(email: str, password: str, role: str):
    """
    Creates a new user in the Cognito Pool.

    ================   ============
    **Endpoint**        /api/users/create
    **Request Type**    POST
    **Access**          ALL
    ================   ============


    Parameters
    -----------
    email : str, required
        The email of the user.
    password : str, required
        The raw password of the user.
    role : str, required
        Specified role of the user.

    Returns
    --------
    UserCreationSuccess : Response
    code
       200
    message
        The user has been successfully created.

    EmailInUse : Response
    code
       400
    message
        This email is already being used.
    """


def delete_user(email: str, auth_token: str):
    """
    Deletes a user specified by their email.

    ================   ============
    **Endpoint**        /api/users/delete
    **Request Type**    POST
    **Access**          MANAGER
    ================   ============

    Parameters
    -----------
    email : str, required
        The email of the user.
    auth_token : str, required
        Token to verify user credentials.

    Returns
    --------
    SuccessfulDelete : Response
    code
       200
    message
        Success

    FailedDelete : Response
    code
       404
    message
        Unauthorized.

    """
