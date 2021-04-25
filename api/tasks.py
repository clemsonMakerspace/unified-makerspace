"""
The Makerspace staff is able to manage maintenance tasks
so that equipment can be repaired in a timely manner.
"""

import models


def get_tasks(auth_token: str):
    """
    Gets all tasks.

    ================   ============
    **Endpoint**        /api/tasks
    **Request Type**    GET
    **Access**          MAINTAINER
    ================   ============


    Parameters
    ------------
    auth_token : str, required
        Token to verify user credentials.

    Returns
    -------
    Success
    code: int
        Return Code
    tasks: [models.Task]
        List of tasks.

    """


def create_task(auth_token: str, task: models.Task):
    """
    Creates a new task.`task` may not have valid `status` or `task_id`.

    ================   ============
    **Endpoint**        /api/tasks
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
    Success
    code: int
        Return Code
    task_id: str
        Task_id of newly created task.

    """


def resolve_task(auth_token: str, task_id: str):
    """
    Resolves or completes a task.

    Notes
    -----
    This does **not** delete the task from the database. It
    only marks it as *resolved*.

    ================   ============
    **Endpoint**        /api/tasks
    **Request Type**    DELETE
    **Access**          MAINTAINER
    ================   ============

    Parameters
    ----------
    auth_token : str, required
        Token to verify user credentials.
    task_id: str, required
        The id of the task to be deleted.


    Returns
    -------
    Success
    code: int
        Return Code
    message: str
    """


def update_task(auth_token: str, task: models.Task):
    """
    Updates a task.

    ================   ============
    **Endpoint**        /api/tasks
    **Request Type**    PATCH
    **Access**          MAINTAINER
    ================   ============

    Parameters
    ----------
    auth_token : str, required
        Token to verify user credentials.
    task: models.Task, required
        The task to be updated.

    Returns
    -------
    Success
    code: int
        Return Code
    message: str
    """
