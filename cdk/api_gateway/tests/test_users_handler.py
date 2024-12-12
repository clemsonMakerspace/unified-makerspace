from moto import mock_aws
import pytest

# Lambda code imports
from ..lambda_code.users_handler.users_handler import UsersHandler
from ..lambda_code.api_defaults import (
    PRIMARY_KEY,
    users_path,
    users_param_path,
)

# Test util imports
from ..utilsFolder.utils import (
    create_table,
    create_rest_http_event,
    jsonify_response,
    get_all_table_items,
    put_all_items_in_table
)


def generate_request_body(rest_method: str,
                          user_id: str = "",
                          university_status: str = "",
                          undergraduate_class: str = "",
                          major: str = ""
                          ) -> dict:

    # Get arguments: values for arguments that don't have an "empty" value
    body: dict = {key: value for key, value in locals().items() if value}

    # Remove user_id if method is PATCH
    if rest_method == "PATCH":
        if 'user_id' in body:
            del body['user_id']

    # No request body should have the rest_method in it
    del body['rest_method']

    # Return request body
    return body

def generate_items(rest_method: str,
                   user_ids: list[str],
                   statuses: list[str],
                   undergrad_classes: list[str],
                   majors: list[str]
                   ) -> list[dict]:
    
    items: list[dict] = []

    for i in range(len(user_ids)):
        user_id = user_ids[i]
        university_status = statuses[i]
        undergrad_class = undergrad_classes[i]
        major = majors[i]

        item = generate_request_body(
                rest_method,
                user_id,
                university_status,
                undergraduate_class=undergrad_class,
                major=major
        )

        items.append(item)

    return items

def create_get_all_event_context():

    event = create_rest_http_event(
        httpMethod = "GET",
        resource = users_path
    )
    context = None

    return (event, context)

def create_get_all_limited_event_contex(limit: int):

    query_parameters: dict = {
        'limit': limit,
    }

    event = create_rest_http_event(
        httpMethod = "GET",
        resource = users_path,
        queryStringParameters=query_parameters,
    )
    context = None

    return (event, context)

def create_post_user_event_contex(request_body: dict) -> tuple:
    event = create_rest_http_event(
        httpMethod = "POST",
        resource = users_path,
        body = request_body,
    )
    context = None

    return (event, context)

def create_get_user_event_contex(user_id: str):

    path_parameters: dict = {
        'user_id': user_id
    }

    event = create_rest_http_event(
        httpMethod = "GET",
        resource = users_param_path,
        pathParameters = path_parameters
    )
    context = None

    return (event, context)

def create_patch_user_event_contex(user_id: str, request_body: dict):
    path_parameters: dict = {
        'user_id': user_id
    }

    event = create_rest_http_event(
        httpMethod = "PATCH",
        resource = users_param_path,
        pathParameters = path_parameters,
        body = request_body,
    )
    context = None

    return (event, context)


@mock_aws
class TestUsers():
    """
    Class to test the users_handler of the backend api. 

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
    def get_user_handler(self):
        """
        Creates a new 'users' dynamodb table, provides this table
        to a UsersHandler, and yields the new UsersHandler to the
        test function. Yielding allows for the table to persist
        through to the test function; otherwise, the mock_aws
        decorator would "tear down the environment", thus preventing
        the table from existing, and causing the UsersHandler to error
        due to not finding the expected resource.

        Because the fixture is not set to the whole module, this means
        each test will need to instantiate -- and add base data to the
        table -- individually. A global UsersHandler can be set for all
        tests by specifying a scope greater than or equal to "class".
        E.g., "class", "module", "package", and "session" will all cause
        the same UsersHandler to be yielded to all tests using this fixture.

        Example:
        @pytest.fixture(scope="module")

        :yields: The tuple (user_handler, dynamodb.Table)
        """

        with mock_aws():
            # Instantiate users table and handler
            table_name: str = "users"
            table = create_table(table_name, PRIMARY_KEY)

            # Setup the users handler
            user_handler = UsersHandler(table)
            yield (user_handler, table)


    def test_get_all_users(self, get_user_handler):
        """
        Tests for a successful response with a 'users' field in the
        response 'body' with a list of users.
        """

        # Get the user handler to use.
        user_handler, table = get_user_handler

        # Create some test users
        user_ids: list[str] = ["test1"]
        statuses: list[str] = ["faculty"]
        undergrad_classes: list[str] = [""]
        majors: list[str] = [""]

        put_items: list[dict] = generate_items(
                "POST",
                user_ids,
                statuses,
                undergrad_classes,
                majors
        )

        # Put them into the table
        put_all_items_in_table(table, put_items)

        # Create the event and context of a get all request
        event, context = create_get_all_event_context()

        # Simulate handling the event
        response = user_handler.handle_event(event, context)
        response = jsonify_response(response)

        # Get values to check from response
        statusCode = response['statusCode']
        body = response['body']

        assert statusCode == 200
        assert "users" in body
        assert type(body['users']) == list
        assert len(body['users']) > 0


    def test_get_all_users_with_limit(self, get_user_handler):
        """
        Tests for a successful response with a 'users' field with a list
        of objects. Checks that the number of items returned is less than
        or equal to the passed in limit.
        """

        # Get the user handler to use.
        user_handler, table = get_user_handler

        # Create some test users
        user_ids: list[str] = ["test1", "test2"]
        statuses: list[str] = ["Faculty", "Undergraduate"]
        undergrad_classes: list[str] = ["", "Senior"]
        majors: list[str] = ["", "Computer Science"]

        put_items: list[dict] = generate_items(
                "POST",
                user_ids,
                statuses,
                undergrad_classes,
                majors
        )

        # Put them into the table
        put_all_items_in_table(table, put_items)

        # Create the event and context with a limit of 1 in the query parameters
        limit: int = 1
        event, context = create_get_all_limited_event_contex(limit)

        # Simulate handling the event
        response = user_handler.handle_event(event, context)
        response = jsonify_response(response)

        # Get values to check from response
        statusCode = response['statusCode']
        body = response['body']

        assert statusCode == 200
        assert "users" in body
        assert type(body['users']) == list
        assert len(body['users']) <= limit


    def test_post_new_user_faculty(self, get_user_handler):
        """
        Tests for the successful creation of a new faculty user.
        """

        # Get the user handler to use.
        user_handler, table = get_user_handler

        # Generate a new faculty user
        user_id: str = "test"
        university_status = "Faculty"
        request_body: dict = generate_request_body(
                "POST",
                user_id,
                university_status=university_status
        )

        # Create the post event and context for the new user
        event, context = create_post_user_event_contex(request_body)

        # Simulate handling the event
        response = user_handler.handle_event(event, context)

        # Get values to check from response
        statusCode = response['statusCode']

        assert statusCode == 201

        # Ensure there is exactly one new item in the table
        data: dict = get_all_table_items(table)
        items: list = data['items']
        assert len(items) == 1

        # Check that the item matches was posted
        item: dict = items[0]
        assert item["user_id"] == user_id
        for key in request_body:
            assert key in item
            assert request_body[key] == item[key]


    def test_get_user(self, get_user_handler):
        """
        Tests for a successful get response when requesting a specific
        user.
        """

        # Get the user handler to use.
        user_handler, table = get_user_handler

        # Create the test user
        user_id: str = "test1"
        university_status: str = "Faculty"
        undergrad_class: str = ""
        major: str = ""

        put_items: list[dict] = generate_items(
                "POST",
                [user_id],
                [university_status],
                [undergrad_class],
                [major]
        )

        # Put them into the table
        put_all_items_in_table(table, put_items)

        # Create the event and context of a get user
        event, context = create_get_user_event_contex(user_id)

        # Simulate handling the event
        response = user_handler.handle_event(event, context)
        response = jsonify_response(response)

        # Get values to check from response
        statusCode = response['statusCode']
        body = response['body']

        assert statusCode == 200

        user_handler.validateUserRequestBody(body)

        assert body['user_id'] == user_id
        assert body['university_status'] == university_status


    def test_patch_user(self, get_user_handler):
        """
        Tests that a patch request updates the matched user's
        information.
        """

        # Get the user handler to use.
        user_handler, table = get_user_handler

        # Create the test user
        user_id: str = "test1"
        university_status: str = "Faculty"
        undergrad_class: str = ""
        major: str = ""

        put_items: list[dict] = generate_items(
                "POST",
                [user_id],
                [university_status],
                [undergrad_class],
                [major]
        )

        # Put them into the table
        put_all_items_in_table(table, put_items)

        # Prepare a patch body to update university_status and major
        new_university_status: str = "Graduate"
        new_major: str = "Computer Science"
        request_body: dict = generate_request_body(
                "PATCH",
                university_status=new_university_status,
                major=new_major
        )

        # Create the post event and context for the new user
        event, context = create_patch_user_event_contex(user_id, request_body)

        # Simulate handling the event
        response = user_handler.handle_event(event, context)

        # Get values to check from response
        statusCode = response['statusCode']

        assert statusCode == 204

        # Ensure the data was successfully updated
        data: dict = get_all_table_items(table)
        item: dict = data['items'][0]

        user_handler.validateUserRequestBody(item)

        assert 'major' in item
        assert item['user_id'] == user_id
        assert item['university_status'] == new_university_status
        assert item['major'] == new_major
