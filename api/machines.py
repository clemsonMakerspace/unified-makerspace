"""
The MakerSpace team can quickly get an overview of the status of all MakerSpace equipment.
"""

def get_machines_status(auth_token: str, start_date: str, end_date: str):
    """
    Gets the status for all machines within the given timeframe.

    ================   ============
    **Endpoint**        /api/machines
    **Request Type**    GET
    **Access**          MANAGER, PUBLIC
    ================   ============

    Parameters
    ----------
    auth_token : str, required
        Token to verify user credentials.
    start_date: str, required
        The start date (inclusive) of the time frame.
    end_date: str, optional
        The end date (inclusive) of the time frame. If not specified,
        all requests until *now* are fetched.

    Notes
    -----
    If accessed with a public *auth_token*, returns only non-sensitive
    machine information.

    Returns
    -------
    Success
    code: int
        Return Code
    machines: [model.Machine]
        List of machines with their statuses.

    """

