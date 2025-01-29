import json
from moto import mock_aws
import pytest
from datetime import datetime

# Lambda code imports
from ..lambda_code.equipment_handler.equipment_handler import (
    EquipmentHandler,
    EQUIPMENT_NAMES,
)

from ..lambda_code.api_defaults import (
    PRIMARY_KEY,
    equipment_path,
    equipment_param_path,
    TIMESTAMP_FORMAT,
)

# Test util imports
from ..utilsFolder.utils import (
    create_gsi_table,
    create_rest_http_event,
    jsonify_response,
    get_all_table_items,
    put_all_items_in_table
)


def generate_request_body(rest_method: str,
                          user_id: str = "",
                          timestamp: str = "",
                          location: str = "",
                          project_name: str = "",
                          project_type: str = "",
                          equipment_type: str = "",
                          class_number: str = "",
                          faculty_name: str = "",
                          project_sponsor: str = "",
                          organization_affiliation: str = "",
                          printer_3d_info: dict = {}
                          ) -> dict:

    # Get arguments: values for arguments that don't have an "empty" value
    kwargs: dict = {key: value for key, value in locals().items() if value}

    ## Handle moving data from 'printer_3d_info' key to 'printer_3d_info'
    #if 'printer_3d_info' in kwargs:
    #    kwargs['printer_3d_info'] = kwargs['printer_3d_info']
    #    del kwargs['printer_3d_info']

    if rest_method == "POST":
        # Get every key: value pair in the arguments
        body: dict = kwargs
    else:
        # Get every key: value pair in the arguments except for user_id
        body: dict = kwargs
        if 'user_id' in body:
            del body['user_id']

    # No request body should have the rest_method in it
    del body['rest_method']

    # Return request body
    return body

def generate_items(rest_method: str,
                   user_ids: list[str],
                   timestamps: list[str],
                   locations: list[str],
                   project_names: list[str],
                   project_types: list[str],
                   equipment_types: list[str],
                   *,
                   class_numbers: list[str] = [],
                   faculty_names: list[str] = [],
                   project_sponsors: list[str] = [],
                   organization_affiliations: list[str] = [],
                   printer_3d_infos: dict = {}
                   ) -> list[dict]:
    
    items: list[dict] = []

    for i in range(len(user_ids)):
        user_id = user_ids[i]
        timestamp = timestamps[i]
        location = locations[i]
        project_name = project_names[i]
        project_type = project_types[i]
        equipment_type = equipment_types[i]
        class_number = class_numbers[i]
        faculty_name = faculty_names[i]
        project_sponsor = project_sponsors[i]
        organization_affiliation = organization_affiliations[i]
        try:
            printer_3d_info = printer_3d_infos[user_id]
        except:
            printer_3d_info = {}

        item = generate_request_body(
                rest_method,
                user_id,
                timestamp,
                location,
                project_name,
                project_type,
                equipment_type,
                class_number=class_number,
                faculty_name=faculty_name,
                project_sponsor=project_sponsor,
                organization_affiliation=organization_affiliation,
                printer_3d_info=printer_3d_info,
        )

        items.append(item)

    return items

def create_get_all_event_context():

    event = create_rest_http_event(
        httpMethod = "GET",
        resource = equipment_path
    )
    context = None

    return (event, context)

def create_get_all_limited_event_contex(limit: int):

    query_parameters: dict = {
        'limit': limit,
    }

    event = create_rest_http_event(
        httpMethod = "GET",
        resource = equipment_path,
        queryStringParameters=query_parameters,
    )
    context = None

    return (event, context)

def create_post_equipment_event_contex(request_body: dict) -> tuple:
    event = create_rest_http_event(
        httpMethod = "POST",
        resource = equipment_path,
        body = request_body,
    )
    context = None

    return (event, context)

def create_get_user_equipment_event_contex(user_id: str):

    path_parameters: dict = {
        'user_id': user_id
    }

    event = create_rest_http_event(
        httpMethod = "GET",
        resource = equipment_param_path,
        pathParameters = path_parameters
    )
    context = None

    return (event, context)

def create_patch_user_equipment_event_contex(user_id: str, request_body: dict):
    path_parameters: dict = {
        'user_id': user_id
    }

    event = create_rest_http_event(
        httpMethod = "PATCH",
        resource = equipment_param_path,
        pathParameters = path_parameters,
        body = request_body,
    )
    context = None

    return (event, context)


@mock_aws
class TestEquipment():
    """
    Class to test the equipment_handler of the backend api. 

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
    def get_equipment_handler(self):
        """
        Creates a new 'equipment' dynamodb table, provides this table
        to an EquipmentHandler, and yields the new EquipmentHandler to the
        test function. Yielding allows for the table to persist
        through to the test function; otherwise, the mock_aws
        decorator would "tear down the environment", thus preventing
        the table from existing, and causing the EquipmentHandler to error
        due to not finding the expected resource.

        Because the fixture is not set to the whole module, this means
        each test will need to instantiate -- and add base data to the
        table -- individually. A global EquipmentHandler can be set for all
        tests by specifying a scope greater than or equal to "class".
        E.g., "class", "module", "package", and "session" will all cause
        the same EquipmentHandler to be yielded to all tests using this fixture.

        Example:
        @pytest.fixture(scope="module")

        :yields: The tuple (equipment_handler, dynamodb.Table)
        """

        with mock_aws():
            # Instantiate users table and handler
            table_name: str = "equipment"
            table = create_gsi_table(table_name, PRIMARY_KEY, "timestamp")

            # Setup the users handler
            equipment_handler = EquipmentHandler(table)
            yield (equipment_handler, table)


    def test_get_all_equipment_logs(self, get_equipment_handler):
        """
        Tests for a successful response with a 'equipment_logs' field in the
        response 'body' with a list of equipment_logs.
        """

        # Get the equipment handler to use.
        equipment_handler, table = get_equipment_handler

        # Create some test equipment logs
        user_ids: list[str] = ["test1"]
        timestamps: list[str] = [datetime.now().strftime(TIMESTAMP_FORMAT)]
        locations: list[str] = ["Watt"]
        project_names: list[str] = ["test"]
        project_types: list[str] = ["Personal"]
        equipment_types: list[str] = [EQUIPMENT_NAMES["LASER_ENGRAVER_STRING"]]
        class_numbers: list[str] = [""]
        faculty_names: list[str] = [""]
        project_sponsors: list[str] = [""]
        organization_affiliations: list[str] = [""]
        printer_3d_infos: dict = {}

        put_items: list[dict] = generate_items(
                "POST",
                user_ids,
                timestamps,
                locations,
                project_names,
                project_types,
                equipment_types,
                class_numbers=class_numbers,
                faculty_names=faculty_names,
                project_sponsors=project_sponsors,
                organization_affiliations=organization_affiliations,
                printer_3d_infos=printer_3d_infos,
        )

        # Put them into the table
        put_all_items_in_table(table, put_items)

        # Create the event and context of a get all request
        event, context = create_get_all_event_context()

        # Simulate handling the event
        response = equipment_handler.handle_event(event, context)
        response = jsonify_response(response)

        # Get values to check from response
        statusCode = response['statusCode']
        body = response['body']

        assert statusCode == 200
        assert "equipment_logs" in body
        assert type(body['equipment_logs']) == list
        assert len(body['equipment_logs']) > 0


    def test_get_all_equipment_with_limit(self, get_equipment_handler):
        """
        Tests for a successful response with a 'equipment_logs' field with a list
        of objects. Checks that the number of items returned is less than
        or equal to the passed in limit.
        """

        # Get the equipment handler to use.
        equipment_handler, table = get_equipment_handler

        # Create some test equipment logs
        user_ids: list[str] = ["test1"]
        timestamps: list[str] = [datetime.now().strftime(TIMESTAMP_FORMAT)]
        locations: list[str] = ["Watt"]
        project_names: list[str] = ["test"]
        project_types: list[str] = ["Personal"]
        equipment_types: list[str] = [EQUIPMENT_NAMES["LASER_ENGRAVER_STRING"]]
        class_numbers: list[str] = [""]
        faculty_names: list[str] = [""]
        project_sponsors: list[str] = [""]
        organization_affiliations: list[str] = [""]
        printer_3d_infos: dict = {}

        put_items: list[dict] = generate_items(
                "POST",
                user_ids,
                timestamps,
                locations,
                project_names,
                project_types,
                equipment_types,
                class_numbers=class_numbers,
                faculty_names=faculty_names,
                project_sponsors=project_sponsors,
                organization_affiliations=organization_affiliations,
                printer_3d_infos=printer_3d_infos,
        )

        # Put them into the table
        put_all_items_in_table(table, put_items)

        # Create the event and context with a limit of 1 in the query parameters
        limit: int = 1
        event, context = create_get_all_limited_event_contex(limit)

        # Simulate handling the event
        response = equipment_handler.handle_event(event, context)
        response = jsonify_response(response)

        # Get values to check from response
        statusCode = response['statusCode']
        body = response['body']

        assert statusCode == 200
        assert "equipment_logs" in body
        assert type(body['equipment_logs']) == list
        assert len(body['equipment_logs']) <= limit


    def test_post_new_equipment_log(self, get_equipment_handler):
        """
        Tests for the successful creation of a new equipment log.
        """

        # Get the equipment handler to use.
        equipment_handler, table = get_equipment_handler

        # Generate a new equipment log
        user_id: str = "test1"
        timestamp: str = datetime.now().strftime(TIMESTAMP_FORMAT)
        location: str = "Watt"
        project_name: str = "test"
        project_type: str = "Personal"
        equipment_type: str = EQUIPMENT_NAMES["LASER_ENGRAVER_STRING"]

        request_body: dict = generate_request_body(
                "POST",
                user_id,
                timestamp,
                location,
                project_name,
                project_type,
                equipment_type,
        )

        # Create the post event and context for the new equipment log
        event, context = create_post_equipment_event_contex(request_body)

        # Simulate handling the event
        response = equipment_handler.handle_event(event, context)

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

    def test_post_valid_fdm_printer_equipment_log(self, get_equipment_handler):
        """
        Tests for the successful creation of a new and valid fdm 3d
        printer equipment log.
        """

        # Get the equipment handler to use.
        equipment_handler, table = get_equipment_handler

        # Generate a new equipment log
        user_id: str = "test1"
        timestamp: str = datetime.now().strftime(TIMESTAMP_FORMAT)
        location: str = "Watt"
        project_name: str = "test"
        project_type: str = "Personal"
        equipment_type: str = EQUIPMENT_NAMES["FDM_PRINTER_STRING"]
        printer_3d_info: dict = {
            "printer_name": "test-printer",
            "print_name": "test print",
            "print_duration": "5",
            "print_status": "In Progress",
            "print_notes": "",
            "print_mass_estimate": "5"
        }

        request_body: dict = generate_request_body(
                "POST",
                user_id,
                timestamp,
                location,
                project_name,
                project_type,
                equipment_type,
                printer_3d_info=printer_3d_info,
        )

        # Create the post event and context for the new equipment log
        event, context = create_post_equipment_event_contex(request_body)

        # Simulate handling the event
        response = equipment_handler.handle_event(event, context)

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

    def test_post_valid_sla_printer_equipment_log(self, get_equipment_handler):
        """
        Tests for the successful creation of a new and valid sla 3d
        printer equipment log.
        """

        # Get the equipment handler to use.
        equipment_handler, table = get_equipment_handler

        # Generate a new equipment log
        user_id: str = "test1"
        timestamp: str = datetime.now().strftime(TIMESTAMP_FORMAT)
        location: str = "Watt"
        project_name: str = "test"
        project_type: str = "Personal"
        equipment_type: str = EQUIPMENT_NAMES["SLA_PRINTER_STRING"]
        printer_3d_info: dict = {
            "printer_name": "test-printer",
            "print_name": "test print",
            "print_duration": "5",
            "print_status": "In Progress",
            "print_notes": "",
            "resin_volume": "5",
            "resin_type": "test type",
        }

        request_body: dict = generate_request_body(
                "POST",
                user_id,
                timestamp,
                location,
                project_name,
                project_type,
                equipment_type,
                printer_3d_info=printer_3d_info,
        )

        # Create the post event and context for the new equipment log
        event, context = create_post_equipment_event_contex(request_body)

        # Simulate handling the event
        response = equipment_handler.handle_event(event, context)

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

    def test_post_invalid_printer_equipment_log(self, get_equipment_handler):
        """
        Tests that a missing field from the printer_3d_info object causes
        the POST request to invalidate.
        """

        # Get the equipment handler to use.
        equipment_handler, table = get_equipment_handler

        # Generate a new equipment log
        user_id: str = "test1"
        timestamp: str = datetime.now().strftime(TIMESTAMP_FORMAT)
        location: str = "Watt"
        project_name: str = "test"
        project_type: str = "Personal"
        equipment_type: str = EQUIPMENT_NAMES["SLA_PRINTER_STRING"]
        printer_3d_info: dict = {
            "printer_name": "test-printer",
            "print_name": "test print",
            # "print_duration": "5", # Simulate missing the print_duration field
            "print_status": "In Progress",
            "print_notes": "",
            "resin_volume": "5",
            "resin_type": "test type",
        }

        request_body: dict = generate_request_body(
                "POST",
                user_id,
                timestamp,
                location,
                project_name,
                project_type,
                equipment_type,
                printer_3d_info=printer_3d_info,
        )

        # Create the post event and context for the new equipment log
        event, context = create_post_equipment_event_contex(request_body)

        # Simulate handling the event
        response = equipment_handler.handle_event(event, context)

        # Get values to check from response
        statusCode = response['statusCode']

        assert statusCode == 400

        # Ensure there are no items in the table
        data: dict = get_all_table_items(table)
        items: list = data['items']
        assert len(items) == 0

    def test_get_user_equipment_logs(self, get_equipment_handler):
        """
        Tests for a successful get response when requesting a specific
        user's equipment logs.
        """

        # Get the equipment handler to use.
        equipment_handler, table = get_equipment_handler

        # Create some test equipment logs
        user_id: str = "test1"
        timestamp: str = datetime.now().strftime(TIMESTAMP_FORMAT)
        location: str = "Watt"
        project_name: str = "test"
        project_type: str = "Personal"
        equipment_type: str = EQUIPMENT_NAMES["LASER_ENGRAVER_STRING"]
        class_number: str = ""
        faculty_name: str = ""
        project_sponsor: str = ""
        organization_affiliation: str = ""
        printer_3d_info: dict = {}

        put_items: list[dict] = generate_items(
                "POST",
                [user_id],
                [timestamp],
                [location],
                [project_name],
                [project_type],
                [equipment_type],
                class_numbers=[class_number],
                faculty_names=[faculty_name],
                project_sponsors=[project_sponsor],
                organization_affiliations=[organization_affiliation],
                printer_3d_infos=printer_3d_info,
        )

        # Build a POST request body to test later that what is returned
        # is the same as the "POST" that would have put it there.
        request_body: dict = generate_request_body(
                "POST",
                user_id,
                timestamp,
                location,
                project_name,
                project_type,
                equipment_type,
        )

        # Put them into the table
        put_all_items_in_table(table, put_items)

        # Create the event and context of a get equipment
        event, context = create_get_user_equipment_event_contex(user_id)

        # Simulate handling the event
        response = equipment_handler.handle_event(event, context)
        response = jsonify_response(response)

        # Get values to check from response
        statusCode = response['statusCode']
        body = response['body']

        assert statusCode == 200
        assert 'equipment_logs' in body
        assert len(body['equipment_logs']) == 1
        equipment_log: dict = body['equipment_logs'][0]

        equipment_handler.validateEquipmentRequestBody(equipment_log)

        assert equipment_log["user_id"] == user_id
        for key in request_body:
            assert key in equipment_log
            assert request_body[key] == equipment_log[key]


    def test_patch_equipment_log(self, get_equipment_handler):
        """
        Tests that a patch request updates the matched equipment
        log.
        """

        # Get the equipment handler to use.
        equipment_handler, table = get_equipment_handler

        # Create some test equipment logs
        user_id: str = "test1"
        timestamp: str = datetime.now().strftime(TIMESTAMP_FORMAT)
        location: str = "Watt"
        project_name: str = "test"
        project_type: str = "Personal"
        equipment_type: str = EQUIPMENT_NAMES["LASER_ENGRAVER_STRING"]
        class_number: str = ""
        faculty_name: str = ""
        project_sponsor: str = ""
        organization_affiliation: str = ""
        printer_3d_info: dict = {}

        put_items: list[dict] = generate_items(
                "POST",
                [user_id],
                [timestamp],
                [location],
                [project_name],
                [project_type],
                [equipment_type],
                class_numbers=[class_number],
                faculty_names=[faculty_name],
                project_sponsors=[project_sponsor],
                organization_affiliations=[organization_affiliation],
                printer_3d_infos=printer_3d_info,
        )

        # Put it into the table
        put_all_items_in_table(table, put_items)

        # Prepare a patch body to update project name
        new_project_name: str = "patch"
        patch_body: dict = generate_request_body(
                "PATCH",
                project_name=new_project_name,
        )

        # Build a POST request body to test later that what is returned
        # is the same as the "POST" that would have put it there.
        expected_body: dict = generate_request_body(
                "POST",
                user_id,
                timestamp,
                location,
                new_project_name,
                project_type,
                equipment_type,
        )

        # Create the post event and context for the new equipment log
        event, context = create_patch_user_equipment_event_contex(user_id, patch_body)

        # Simulate handling the event
        response = equipment_handler.handle_event(event, context)

        # Get values to check from response
        statusCode = response['statusCode']

        assert statusCode == 204

        # Ensure the data was successfully updated
        data: dict = get_all_table_items(table)
        equipment_log: dict = data['items'][0]

        equipment_handler.validateEquipmentRequestBody(equipment_log)

        assert equipment_log["user_id"] == user_id
        for key in expected_body:
            assert key in equipment_log
            assert expected_body[key] == equipment_log[key]
