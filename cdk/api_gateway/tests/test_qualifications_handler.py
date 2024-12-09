import json
from moto import mock_aws
import pytest
from datetime import datetime, timedelta

# Lambda code imports
from lambda_code.qualifications_handler.qualifications_handler import QualificationsHandler
from lambda_code.api_defaults import (
    PRIMARY_KEY,
    qualifications_path,
    qualifications_param_path,
    TIMESTAMP_FORMAT,
)

# Test util imports
from tests.utils.utils import (
    create_gsi_table,
    create_rest_http_event,
    jsonify_response,
    get_all_table_items,
    put_all_items_in_table
)


def generate_request_body(rest_method: str,
                          user_id: str = "",
                          last_updated: str = "",
                          trainings: list[dict] = [],
                          waivers: list[dict] = [],
                          miscellaneous: list[dict] = [],
                          ) -> dict:

    body = locals()

    if rest_method == "PATCH":
        # user_id should never be in patch body
        if 'user_id' in body:
            del body['user_id']

    # No request body should have the rest_method in it
    del body['rest_method']

    # Return request body
    return body

def generate_items(rest_method: str,
                   user_ids: list[str] = [],
                   last_updateds: list[str] = [],
                   trainings: list[list[dict]] = [],
                   waivers: list[list[dict]] = [],
                   miscellaneous: list[list[dict]] = [],
                   ) -> list[dict]:
    
    items: list[dict] = []

    for i in range(len(user_ids)):
        user_id = user_ids[i]
        last_updated = last_updateds[i]
        training = trainings[i]
        waiver = waivers[i]
        misc = miscellaneous[i]

        item = generate_request_body(
                rest_method,
                user_id,
                last_updated,
                training,
                waiver,
                misc
        )

        items.append(item)

    return items

def create_get_all_event_context():

    event = create_rest_http_event(
        httpMethod = "GET",
        resource = qualifications_path
    )
    context = None

    return (event, context)

def create_get_all_limited_event_contex(limit: int):

    query_parameters: dict = {
        'limit': limit,
    }

    event = create_rest_http_event(
        httpMethod = "GET",
        resource = qualifications_path,
        queryStringParameters=query_parameters,
    )
    context = None

    return (event, context)

def create_post_qualifications_event_contex(request_body: dict) -> tuple:
    event = create_rest_http_event(
        httpMethod = "POST",
        resource = qualifications_path,
        body = request_body,
    )
    context = None

    return (event, context)

def create_get_user_qualifications_event_contex(user_id: str):

    path_parameters: dict = {
        'user_id': user_id
    }

    event = create_rest_http_event(
        httpMethod = "GET",
        resource = qualifications_param_path,
        pathParameters = path_parameters
    )
    context = None

    return (event, context)

def create_patch_user_qualifications_event_contex(user_id: str, request_body: dict):
    path_parameters: dict = {
        'user_id': user_id
    }

    event = create_rest_http_event(
        httpMethod = "PATCH",
        resource = qualifications_param_path,
        pathParameters = path_parameters,
        body = request_body,
    )
    context = None

    return (event, context)


@mock_aws
class TestQualifications():
    """
    Class to test the qualifications_handler of the backend api. 

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
    def get_qualifications_handler(self):
        """
        Creates a new 'qualifications' dynamodb table, provides this table
        to an QualificationsHandler, and yields the new QualificationsHandler to the
        test function. Yielding allows for the table to persist
        through to the test function; otherwise, the mock_aws
        decorator would "tear down the environment", thus preventing
        the table from existing, and causing the QualificationsHandler to error
        due to not finding the expected resource.

        Because the fixture is not set to the whole module, this means
        each test will need to instantiate -- and add base data to the
        table -- individually. A global QualificationsHandler can be set for all
        tests by specifying a scope greater than or equal to "class".
        E.g., "class", "module", "package", and "session" will all cause
        the same QualificationsHandler to be yielded to all tests using this fixture.

        Example:
        @pytest.fixture(scope="module")

        :yields: The tuple (qualifications_handler, dynamodb.Table)
        """

        with mock_aws():
            # Instantiate users table and handler
            table_name: str = "qualifications"
            table = create_gsi_table(table_name, PRIMARY_KEY, "last_updated")

            # Setup the users handler
            qualifications_handler = QualificationsHandler(table)
            yield (qualifications_handler, table)


    def test_get_all_qualifications(self, get_qualifications_handler):
        """
        Tests for a successful response with a 'qualifications' field in the
        response 'body' with a list of qualifications.
        """

        # Get the user handler to use.
        qualifications_handler, table = get_qualifications_handler

        # Create some test qualifications logs
        user_ids: list[str] = ["test1"]
        last_updateds: list[str] = [datetime.now().strftime(TIMESTAMP_FORMAT)]
        trainings: list[list[dict]] = [[]]
        waivers: list[list[dict]] = [[]]
        miscellaneous: list[list[dict]] = [[]]

        put_items: list[dict] = generate_items(
                "POST",
                user_ids,
                last_updateds,
                trainings,
                waivers,
                miscellaneous
        )

        # Put them into the table
        put_all_items_in_table(table, put_items)

        # Create the event and context of a get all request
        event, context = create_get_all_event_context()

        # Simulate handling the event
        response = qualifications_handler.handle_event(event, context)
        response = jsonify_response(response)

        # Get values to check from response
        statusCode = response['statusCode']
        body = response['body']

        assert statusCode == 200
        assert "qualifications" in body
        assert type(body['qualifications']) == list
        assert len(body['qualifications']) > 0


    def test_get_all_qualifications_with_limit(self, get_qualifications_handler):
        """
        Tests for a successful response with a 'qualifications' field with a list
        of objects. Checks that the number of items returned is less than
        or equal to the passed in limit.
        """

        # Get the user handler to use.
        qualifications_handler, table = get_qualifications_handler

        # Create some test qualifications logs
        user_ids: list[str] = ["test1"]
        last_updateds: list[str] = [datetime.now().strftime(TIMESTAMP_FORMAT)]
        trainings: list[list[dict]] = [[]]
        waivers: list[list[dict]] = [[]]
        miscellaneous: list[list[dict]] = [[]]

        put_items: list[dict] = generate_items(
                "POST",
                user_ids,
                last_updateds,
                trainings,
                waivers,
                miscellaneous
        )

        # Put them into the table
        put_all_items_in_table(table, put_items)

        # Create the event and context with a limit of 1 in the query parameters
        limit: int = 1
        event, context = create_get_all_limited_event_contex(limit)

        # Simulate handling the event
        response = qualifications_handler.handle_event(event, context)
        response = jsonify_response(response)

        # Get values to check from response
        statusCode = response['statusCode']
        body = response['body']

        assert statusCode == 200
        assert "qualifications" in body
        assert type(body['qualifications']) == list
        assert len(body['qualifications']) <= limit


    def test_post_new_qualifications(self, get_qualifications_handler):
        """
        Tests for the successful creation of a new user's qualifications.
        """

        # Get the user handler to use.
        qualifications_handler, table = get_qualifications_handler

        # Generate a new qualifications log
        user_id: str = "test1"
        last_updated: str = datetime.now().strftime(TIMESTAMP_FORMAT)
        trainings: list[dict] = []
        waivers: list[dict] = []
        miscellaneous: list[dict] = []

        request_body: dict = generate_request_body(
                "POST",
                user_id,
                last_updated,
                trainings,
                waivers,
                miscellaneous
        )

        # Create the post event and context for the new user
        event, context = create_post_qualifications_event_contex(request_body)

        # Simulate handling the event
        response = qualifications_handler.handle_event(event, context)

        # Get values to check from response
        statusCode = response['statusCode']

        assert statusCode == 201

        # Ensure there is exactly one new item in the table
        data: dict = get_all_table_items(table)
        items: list = data['items']
        assert len(items) == 1

        # Check that the item matches what was posted
        item: dict = items[0]
        assert item["user_id"] == user_id
        for key in request_body:
            assert key in item
            assert request_body[key] == item[key]

    def test_get_user_qualifications(self, get_qualifications_handler):
        """
        Tests for a successful get response when requesting a specific
        user's qualifications logs.
        """

        # Get the user handler to use.
        qualifications_handler, table = get_qualifications_handler

        # Generate a new qualifications log
        user_id: str = "test1"
        last_updated: str = datetime.now().strftime(TIMESTAMP_FORMAT)
        trainings: list[dict] = []
        waivers: list[dict] = []
        miscellaneous: list[dict] = []

        put_items: list[dict] = generate_items(
                "POST",
                [user_id],
                [last_updated],
                [trainings],
                [waivers],
                [miscellaneous]
        )

        # Build a POST request body to test later that what is returned
        # is the same as the "POST" that would have put it there.
        request_body: dict = generate_request_body(
                "POST",
                user_id,
                last_updated,
                trainings,
                waivers,
                miscellaneous
        )

        # Put them into the table
        put_all_items_in_table(table, put_items)

        # Create the event and context of a get user
        event, context = create_get_user_qualifications_event_contex(user_id)

        # Simulate handling the event
        response = qualifications_handler.handle_event(event, context)
        response = jsonify_response(response)

        # Get values to check from response
        statusCode = response['statusCode']
        body = response['body']

        assert statusCode == 200

        qualifications_handler.validateQualificationRequestBody(body)

        assert body["user_id"] == user_id
        for key in request_body:
            assert key in body
            assert request_body[key] == body[key]


    def test_patch_qualifications(self, get_qualifications_handler):
        """
        Tests that a patch request updates the matched user's qualifications
        data.
        """

        # Get the user handler to use.
        qualifications_handler, table = get_qualifications_handler

        # Generate a new qualifications log
        user_id: str = "test1"
        last_updated: str = datetime.now().strftime(TIMESTAMP_FORMAT)
        trainings: list[dict] = []
        waivers: list[dict] = []
        miscellaneous: list[dict] = []

        put_items: list[dict] = generate_items(
                "POST",
                [user_id],
                [last_updated],
                [trainings],
                [waivers],
                [miscellaneous]
        )

        # Put it into the table
        put_all_items_in_table(table, put_items)

        # Prepare a patch body to update trainings

        # Need to add an arbitrary timedelta due to nature of qualifications deleting
        # "old" entries that match the same old "last_updated" timestamp.
        new_last_updated: str = (datetime.now() + timedelta(seconds=10)) \
                                .strftime(TIMESTAMP_FORMAT)

        new_trainings: list[dict] = [
                { 'name': "Test Training", "completion_status": "Complete" }
        ]
        patch_body: dict = generate_request_body(
                "PATCH",
                last_updated=new_last_updated,
                trainings=new_trainings
        )

        # Build a POST request body to test later that what is returned
        # is the same as the "POST" that would have put it there.
        expected_body: dict = generate_request_body(
                "POST",
                user_id,
                new_last_updated,
                new_trainings,
                waivers,
                miscellaneous
        )

        # Create the post event and context for the new user
        event, context = create_patch_user_qualifications_event_contex(user_id, patch_body)

        # Simulate handling the event
        response = qualifications_handler.handle_event(event, context)

        # Get values to check from response
        statusCode = response['statusCode']

        assert statusCode == 204

        # Ensure the data was successfully updated
        data: dict = get_all_table_items(table)
        qualifications: dict = data['items'][0]

        qualifications_handler.validateQualificationRequestBody(qualifications)

        assert qualifications["user_id"] == user_id
        for key in expected_body:
            assert key in qualifications
            assert expected_body[key] == qualifications[key]
