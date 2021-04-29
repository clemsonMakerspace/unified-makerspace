"""
The Makerspace is visited by students and faculty
from all walks of life. The API enables the staff to see
who exactly is visiting the Makerspace, if they are a new
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
    Gets all Makerspace visitors within a given timeframe. If neither
    `start_date` or `end_date specified`, get all data.

    Note
    ------
    Returns `visit`, not `visitor`, objects. Name not changed
    to `get_visits` for backwards compatibility.

    ================   ============
    **Endpoint**        /api/visitors
    **Request Type**    POST
    **Access**          MANAGER
    ================   ============

    Parameters
    ----------
    auth_token : str, required
        Token to verify user credentials.
    start_date: str, optional
        The start date (inclusive) of the time frame. If not specified,
        assume the start of time (epoch of 0).
    end_date: str, optional
        The end date (inclusive) of the time frame. If not specified,
        "today" is assumed.

    Note
    -----
    Endpoint returns type `visits`, not `visitors`.

    Returns
    -------
    Success
    code: int
        Return Code
    visitors: [model.Visit]
    """


def get_visitor_data(auth_token: str, visitor_id: str):
    """
    Gets data for visitor specified by `visitor_id`. If
    visitor_id not specified, get data for all visitors.

    Note
    ------
    Returns `visit`, not `visitor`, objects. Name not changed
    to `get_visits` for backwards compatibility.

    ================   ============
    **Endpoint**        /api/visitors
    **Request Type**    POST
    **Access**          MANAGER
    ================   ============

    Parameters
    ----------
    auth_token : str, optional
        Token to verify user credentials.
    visitor_id : str, required
        Visitor to return data for.

    Note
    -----
    Endpoint returns type `visits`, not `visitors`.

    Returns
    -------
    Success
    code: int
        Return Code
    visitor: model.Visitor | [model.Visitor]
    """
