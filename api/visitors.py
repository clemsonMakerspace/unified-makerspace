"""
The MakerSpace is visited by students and faculty
from all walks of life. The API enables the staff to see
who exactly is visiting the MakerSpace, if they are a new
member, and when.
"""
from models import Visitor


def create_visitor(auth_token: str, visitor: Visitor, hardware_id: str):
    """
    Creates a new visitor.

    ================   ============
    **Endpoint**        /api/visitors
    **Request Type**    PUT
    **Access**          ALL
    ================   ============

    Parameters
    ----------
    auth_token : str, required
        Token to verify user credentials.
    visitor : Visitor
        Visitor information.
    hardware_id : str, required
        Unique hardware id of the user's TigerCard.

    Returns
    -------
    Success
    code : str
        Return code.
    message: str
    """

def get_visitors(auth_token: str, start_date: int, end_date: int):
    """
    Gets all MakerSpace visitors within a given timeframe.

    ================   ============
    **Endpoint**        /api/visitors
    **Request Type**    POST
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
