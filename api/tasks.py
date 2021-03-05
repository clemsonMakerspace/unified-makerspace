import models


def create_task(auth_token: str, task: models.Task):
    """
    Creates a task.

    ================   ============
    **Endpoint**        /api/task/create
    **Request Type**    POST
    **Access**          MAINTAINER
    ================   ============


    Parameters
    ----------
    auth_token : str, required
        Token to verify user credentials.

    task: models.Task, required
        The task to create.

    Returns
    -------
    Success: Response

    """


def delete_task(auth_token: str, task_id: str):
    """

    ================   ============
    **Endpoint**        /api/task/delete
    **Request Type**    POST
    **Access**          MAINTAINER
    ================   ============

    Parameters
    ----------
    auth_token
    task_id: str
        The id of the task to be deleted.


    Returns
    -------

    """
    pass


def update_task(auth_token: str, task: models.Task):
    pass
