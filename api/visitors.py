


def get_visitors(auth_id: str, start_date:str, end_date: str):
    """
    Gets all MakerSpace visitors between a certain timeframe.

    ================   ============
    **Endpoint**        /api/visitors
    **Request Type**    GET
    **Access**          MANAGER
    ================   ============


    Parameters
    ----------
    auth_id: str

    start_date
    end_date

    Returns
    -------
    Success: Response
    visitors: [model.Visitor]

    """
