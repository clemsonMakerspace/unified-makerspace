from moto import mock_aws
import pytest
from datetime import datetime

# Lambda code imports
from ..lambda_code.visits_handler.visits_handler import VisitsHandler
from ..lambda_code.api_defaults import (
    PRIMARY_KEY,
    visits_path,
    visits_param_path,
    TIMESTAMP_FORMAT
)

# Test util imports
from ..utilsFolder.utils import (
    create_table,
    create_gsi_table,
    create_ses_client,
    create_rest_http_event,
    jsonify_response,
    get_all_table_items,
    put_all_items_in_table
)


def generate_request_body(user_id: str,
                          timestamp: str,
                          location: str
                          ) -> dict:

    # Get arguments: values for arguments that don't have an "empty" value
    body: dict = {key: value for key, value in locals().items() if value}

    # Return request body
    return body

def generate_items(user_ids: list[str],
                   timestamps: list[str],
                   locations: list[str],
                   ) -> list[dict]:
    
    items: list[dict] = []

    for i in range(len(user_ids)):
        user_id = user_ids[i]
        timestamp = timestamps[i]
        location = locations[i]

        item = generate_request_body(
                user_id,
                timestamp,
                location
        )

        items.append(item)

    return items

def create_get_all_event_context():

    event = create_rest_http_event(
        httpMethod = "GET",
        resource = visits_path
    )
    context = None

    return (event, context)

def create_get_all_limited_event_contex(limit: int):

    query_parameters: dict = {
        'limit': limit,
    }

    event = create_rest_http_event(
        httpMethod = "GET",
        resource = visits_path,
        queryStringParameters=query_parameters,
    )
    context = None

    return (event, context)

def create_post_visit_event_contex(request_body: dict) -> tuple:
    event = create_rest_http_event(
        httpMethod = "POST",
        resource = visits_path,
        body = request_body,
    )
    context = None

    return (event, context)

def create_get_user_visits_event_contex(user_id: str):

    path_parameters: dict = {
        'user_id': user_id
    }

    event = create_rest_http_event(
        httpMethod = "GET",
        resource = visits_param_path,
        pathParameters = path_parameters
    )
    context = None

    return (event, context)

@mock_aws
class TestVisits():
    """
    Class to test the visits_handler of the backend api. 

    Tests follow this general workflow:
    1) Get the handler and table to use for the test.
    2) Optional: Put items into the table as needed.
        Mostly for GET, DELETE, PATCH tests.
    3) Generate an AWS Rest HTTP event (and context).
    4) Send the event and context to the handler, saving the response.
    5) Assert statements based on expected behavior delivered in response
        and/or stored in the table.
    """

    @pytest.fixture
    def get_visit_handler(self):
        """
        Creates a new 'visits' and 'users' dynamodb tables, creates
        an ses client, and provides all of these resources to a
        VisitsHandler, and yields the new VisitsHandler and visits table
        to the test function. Yielding allows for the table to persist
        through to the test function; otherwise, the mock_aws
        decorator would "tear down the environment", thus preventing
        the table from existing, and causing the VisitsHandler to error
        due to not finding the expected resource.

        Because the fixture is not set to the whole module, this means
        each test will need to instantiate -- and add base data to the
        table -- individually. A global VisitsHandler can be set for all
        tests by specifying a scope greater than or equal to "class".
        E.g., "class", "module", "package", and "session" will all cause
        the same VisitsHandler to be yielded to all tests using this fixture.

        Example:
        @pytest.fixture(scope="module")

        :yields: The tuple (visit_handler, dynamodb.Table [visits])
        """

        with mock_aws():
            # Instantiate users table, visits table, ses client, and handler
            users_table_name: str = "users"
            users_table = create_table(users_table_name, PRIMARY_KEY)

            visits_table_name: str = "visits"
            visits_table = create_gsi_table(visits_table_name, PRIMARY_KEY, "timestamp")

            ses = create_ses_client()

            # Setup the users handler
            visit_handler = VisitsHandler(visits_table, users_table, ses)

            yield (visit_handler, visits_table)


    def test_get_all_visits(self, get_visit_handler):
        """
        Tests for a successful response with a 'visits' field in the
        response 'body' with a list of visits.
        """

        # Get the visit handler to use.
        visit_handler, visits_table = get_visit_handler

        # Create some test visits
        user_ids: list[str] = ["test1"]
        timestamps: list[str] = [datetime.now().strftime(TIMESTAMP_FORMAT)]
        locations: list[str] = ["Watt"]

        put_items: list[dict] = generate_items(
                user_ids,
                timestamps,
                locations,
        )

        # Put them into the table
        put_all_items_in_table(visits_table, put_items)

        # Create the event and context of a get all request
        event, context = create_get_all_event_context()

        # Simulate handling the event
        response = visit_handler.handle_event(event, context)
        response = jsonify_response(response)

        # Get values to check from response
        statusCode = response['statusCode']
        body = response['body']

        assert statusCode == 200
        assert "visits" in body
        assert type(body['visits']) == list
        assert len(body['visits']) > 0


    def test_get_all_visits_with_limit(self, get_visit_handler):
        """
        Tests for a successful response with a 'visits' field with a list
        of objects. Checks that the number of items returned is less than
        or equal to the passed in limit.
        """

        # Get the visit handler to use.
        visit_handler, visits_table = get_visit_handler

        # Create some test visits
        user_ids: list[str] = ["test1", "test2"]
        timestamps: list[str] = [
            datetime.now().strftime(TIMESTAMP_FORMAT),
            datetime.now().strftime(TIMESTAMP_FORMAT)
        ]
        locations: list[str] = ["Watt", "Watt"]

        put_items: list[dict] = generate_items(
                user_ids,
                timestamps,
                locations,
        )

        # Put them into the table
        put_all_items_in_table(visits_table, put_items)

        # Create the event and context with a limit of 1 in the query parameters
        limit: int = 1
        event, context = create_get_all_limited_event_contex(limit)

        # Simulate handling the event
        response = visit_handler.handle_event(event, context)
        response = jsonify_response(response)

        # Get values to check from response
        statusCode = response['statusCode']
        body = response['body']

        assert statusCode == 200
        assert "visits" in body
        assert type(body['visits']) == list
        assert len(body['visits']) <= limit


    def test_post_new_visit(self, get_visit_handler):
        """
        Tests for the successful creation of a new visit.
        """

        # Get the visit handler to use.
        visit_handler, visits_table = get_visit_handler

        # Generate a new visit request body
        user_id: str = "test"
        timestamp: str = datetime.now().strftime(TIMESTAMP_FORMAT)
        location: str = "Watt"

        request_body: dict = generate_request_body(
                user_id,
                timestamp,
                location
        )

        # Create the post event and context for the new visit
        event, context = create_post_visit_event_contex(request_body)

        # Simulate handling the event
        response = visit_handler.handle_event(event, context)

        # Get values to check from response
        statusCode = response['statusCode']

        assert statusCode == 201

        # Ensure there is exactly one new item in the table
        data: dict = get_all_table_items(visits_table)
        items: list = data['items']
        assert len(items) == 1

        # Check that the item matches was posted
        item: dict = items[0]
        assert item["user_id"] == user_id
        for key in request_body:
            assert key in item
            assert request_body[key] == item[key]


    def test_get_user_visits(self, get_visit_handler):
        """
        Tests for a successful get response when requesting a specific
        user's visits.
        """

        # Get the visit handler to use.
        visit_handler, visits_table = get_visit_handler

        # Create the test user's visit
        user_id: str = "test1"
        timestamp: str = datetime.now().strftime(TIMESTAMP_FORMAT)
        location: str = "Watt"

        put_items: list[dict] = generate_items(
                [user_id],
                [timestamp],
                [location]
        )

        # Put it into the table
        put_all_items_in_table(visits_table, put_items)

        # Create the event and context of a get user visits
        event, context = create_get_user_visits_event_contex(user_id)

        # Simulate handling the event
        response = visit_handler.handle_event(event, context)
        response = jsonify_response(response)

        # Get values to check from response
        statusCode = response['statusCode']
        body = response['body']

        assert statusCode == 200
        assert 'visits' in body
        assert len(body['visits']) == 1
        visit: dict = body['visits'][0]

        visit_handler.validateVisitRequestBody(visit)

        assert visit['user_id'] == user_id
        assert visit['timestamp'] == timestamp
        assert visit['location'] == location
