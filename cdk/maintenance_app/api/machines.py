"""
The MakerSpace team can quickly get an overview of the status of all MakerSpace equipment.
"""

def get_machines_status(auth_token: str, start_time: int, end_time: int):
    """
    Gets the status for all machines within the given timeframe. Dates are
    expressed in epoch time.

    Notes
    -----
    If accessed with a public *auth_token*, returns only non-sensitive
    machine information.

    .. deprecated:: 5.9.1
         Key is now `statuses` instead of `machines`.


    ================   ============
    **Endpoint**        /api/machines
    **Request Type**    POST
    **Access**          ANY, MANAGER
    ================   ============

    Parameters
    ----------
    auth_token : str, required
        Token to verify user credentials.
    start_time: int, required
        The start date (inclusive) of the time frame.
    end_time: int, optional
        The end date (inclusive) of the time frame. If not specified,
        all requests until *now* are fetched.




    Returns
    -------
    Success
    code: int
        Return Code
    statuses: { str : [(int, int), ...], ... }
        Dictionary mapping the names of each machine to list of tuples
        indicating the start and end times of when the machine was not working.
        Tuples should be chronological. (see `app.py` for an example response).
    """


# todo statuses or machines?

def delete_machine(auth_token: str, machine_name: str):
    """
    Deletes a machine and any associated tasks.

    ================   ============
    **Endpoint**        /api/machines
    **Request Type**    DELETE
    **Access**          MAINTAINER
    ================   ============

    Parameters
    ----------
    auth_token : str, required
        Token to verify user credentials.
    machine_name: str, required
        Name of the machine to be deleted.

    Returns
    -------
    Success
    code: int
        Return Code
    message: str
    """

