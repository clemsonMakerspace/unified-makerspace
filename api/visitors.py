"""
The MakerSpace is visited by students and faculty
from all walks of life. The API enables the staff to see
who exactly is visiting the MakerSpace, if they are a new
member, and when.
"""


def get_visitors(auth_token: str, start_date: str, end_date: str):
    """
    Gets all MakerSpace visitors within a given timeframe.

    ================   ============
    **Endpoint**        /api/visitors
    **Request Type**    GET
    **Access**          MANAGER
    ================   ============

    Parameters
    ----------
    auth_token : str, required
        Token to verify user credentials.
    start_date: str, required
        The start date (inclusive) of the time frame.
    end_date: str, optional
        The end date (inclusive) of the time frame. If not specified,
        "today" is assumed.

    Returns
    -------
    Success
    code: int
        Return Code
    visitors: [model.Visitor]
    """
