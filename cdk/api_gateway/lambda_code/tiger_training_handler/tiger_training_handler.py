import urllib3
import json
import os
import base64
from dataclasses import dataclass, field
from datetime import datetime
import logging
import boto3
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from api_defaults import *

logger = logging.getLogger()
logger.setLevel(logging.INFO)

http = urllib3.PoolManager()

# The bridge timestamp expects the seconds to be in milliseconds (3 decimal places)
BRIDGE_TIMESTAMP_FORMAT: str = "%Y-%m-%dT%H:%M:%S.%f"
# bridge also (as far as observed) only uses the timezone offset of -04:00
TZ_OFFSET: str = "-04:00"
# With all of this together, a valid brige timestamp is in the format:
# BRIDGE_TIMESTAMP_FORMAT + TZ_OFFSET

def create_rest_http_event(httpMethod: str, resource: str,
                      body = {},
                      pathParameters: dict = {},
                      queryStringParameters: dict = {}
                      ) -> dict:
    """
    Creates a Rest HTTP event similar to what ApiGateway will
    send to a lambda proxy. Use to prepare an event an api
    handler would receive and handle.

    :params httpMethod: The http method of the event. One of:
                        "GET", "POST", "PATCH", "PUT", and
                        "DELETE".
    :params resource: The endpoint resource of the api that will
                      be acted on. Path parameters must be named,
                      not resolved, and should be in curly
                      brackets ({}).
                      Example: /test/{test_id}
    :params body: The request json body to be sent.
    :params pathParamters: A dictionary of path parameter names and
                           their values.
    :params queryStringParameters: A dictionary of query parameter
                                   names and their values as strings.
    :returns: A json object representing an AWS ApiGateway event.
    """

    # Stringify the body
    response = locals()
    response['body'] = json.dumps(response['body'])
    return response

@dataclass
class CompletableItem():
    name: str
    completion_status: str


@dataclass
class Learner():
    user_id: str = ""
    last_updated: str = datetime.min.isoformat()
    enrolled_course_statuses: list[CompletableItem] = field(default_factory=list)

    # Class-level variable to store the learner with the latest updated at timestamp
    _latest_timestamp_learner = None

    def is_timestamp_greater_than_class_latest(self, timestamp) -> bool:
        """
        Function to check if a passed in timestamp is greater than the last_updated
        timestamp stored in _latest_timestamp_learner.

        :params timestamp: The timestamp to compare.
        :returns: True if the timestamp paramter is greater, False otherwise.
        """

        # Always True if _latest_timestamp_learner is None
        if Learner._latest_timestamp_learner is None:
            return True

        # Check if timestamp is greater
        elif timestamp > Learner._latest_timestamp_learner.last_updated:
            return True

        # Otherwise return false
        return False
        

    def _update_latest_timestamp_learner(self):
        """
        Tries to update the class-level variable `_latest_timestamp_learner`
        to the current class if it is, in fact, the learner with the latest
        timestamp.
        """

        if self.is_timestamp_greater_than_class_latest(self.last_updated):
            Learner._latest_timestamp_learner = self


    def __post_init__(self):
        """
        Function called after individual class initialization.
        """

        # Try updating latest learner
        self._update_latest_timestamp_learner()


    def add_enrolled_course(self, name: str, completion_status: str):
        """
        Adds a course as a completable item to the learners enrolled
        course statuses.

        :params name: The name of the course.
        :params completion_status: Either "Complete" or "Incomplete" representing
                                   if the course has been completed or not.
        """
        item: CompletableItem = CompletableItem(name, completion_status)
        self.enrolled_course_statuses.append(item)

    def update_timestamp(self, last_updated: str):
        """
        Updates the last_updated timestamp to the greater (latest) timestamp

        :params last_updated: The timestamp should be an EST timestamp in the format
                              "YYYY-MM-DDThh:mm:ss" without regard for timezone
                              offset. 
        """
        # Update the last_updated time to the latest possible time
        if last_updated > self.last_updated:
            self.last_updated = last_updated

        # Try updating latest learner
        self._update_latest_timestamp_learner()



@dataclass
class Course():
    id: int
    name: str

    def get_completed_enrollments(self, bridge_url: str, auth_token: str,
                                  base_time: str, learners: dict[str, Learner]):
        """
        Get all enrollments from the course and add it to a learner's completableitem
        list.

        :params bridge_url: The base url of the api endpoint.
        :params auth_token: The authorization token to use in the request.
        :params base_time: Restricts get response to only include enrollments
                           updated on or after this time.
        :params learners: The dictionary of learners that should be updated
                          for all completed courses.
        """

        # Create endpoint url and prepare necessary headers
        query_parameters: str = f"?updated_after={base_time}"
        endpoint_url: str = f"{bridge_url}/api/author/course_templates"\
                           +f"/{self.id}/enrollments" + query_parameters
        headers: dict = {
            "Authorization": f"Basic {auth_token}"
        }

        # Get the course information
        response = http.request('GET', endpoint_url, headers=headers)
        body = json.loads(response.data)

        # Create learner lookup dictionary
        learner_lookup: dict[str, str] = {}
        # Get the linked learners
        response_learners = body["linked"]["learners"]

        for item in response_learners:
            id: str = item["id"]
            # Parse user_id from returned email
            user_id: str = item["email"].split("@")[0]
            learner_lookup[id] = user_id

        # Go through enrollments and add this course to all learners who have completed it
        enrollments = body["enrollments"]
        for enrollment in enrollments:

            # Get the user_id to use for the learner
            user_id = learner_lookup[enrollment["links"]["learner"]["id"]]

            # Convert updated_at timestamp to TIMESTAMP_FORMAT
            updated_datetime = datetime.fromisoformat(enrollment['updated_at'])
            last_updated = updated_datetime.strftime(TIMESTAMP_FORMAT)

            # Update the learner's enrolled courses if they completed the course
            if enrollment["state"].lower() == "complete":
                # Create new learner if needed
                if user_id not in learners:
                    learners[user_id] = Learner(user_id)

                # Append course
                learners[user_id].add_enrolled_course(self.name, "Complete")

                # Try updating the last_updated timestamp for the learner (and class)
                learners[user_id].update_timestamp(last_updated)

            # Always create a Learner variable in case a user did not complete
            # the course but has the latest last_updated timestamp
            Learner(user_id, last_updated)


@dataclass
class Program():
    id: int
    courses: list[Course] = field(default_factory=list)

    def get_courses(self, bridge_url: str, auth_token: str):
        """
        Retrieves all of the courses contained within the program.

        :params bridge_url: The base url of the api endpoint.
        :params auth_token: The authorization token to use in the request.
        """

        # Create endpoint url and prepare necessary headers
        endpoint_url: str = f"{bridge_url}/api/author/programs/{self.id}"
        headers: dict = {
            "Authorization": f"Basic {auth_token}"
        }

        # Get the program information
        response = http.request('GET', endpoint_url, headers=headers)
        body = json.loads(response.data)

        # Get the list of courses in the program
        course_list: list[dict] = body["programs"][0]["items"]

        # Save necessary information from each course
        for course in course_list:
            id: int = int(course["id"])
            name: str = course["title"]
            self.courses.append(Course(id, name))


def get_auth_token(key: str, secret: str) -> str:
    """
    This method builds the authorization token used when making api calls
    for tiger training (Bridge LMS) given a key and secret.

    :params key: The key for the bridge api auth token.
    :params secret: The secret for the bridge api auth token.
    :returns: The string version of the tiger training api authorization
              token.
    """


    # Encode to authorization token
    combined_string = f"{key}:{secret}"
    b64_bytes = base64.b64encode(combined_string.encode())
    auth_token = b64_bytes.decode()

    return auth_token


def get_pretty_print_json(json_obj: dict) -> str:
    """
    Helper function to print a dictionary object with indentation.

    :returns: A dictionary as a string.
    """
    return json.dumps(json_obj, indent=2)


class TigerTrainingHandler():
    def __init__(self):

        # Bridge API Endpoint
        self.bridge_url = os.environ["BRIDGE_URL"]

        # Get key/secret from environment
        self.key = os.environ["BRIDGE_KEY"]
        self.secret = os.environ["BRIDGE_SECRET"]

        # Get the bridge auth token using api key and secret
        self.bridge_auth_token = get_auth_token(self.key, self.secret)

        # Get the program id from environment
        self.program_id: int = int(os.environ["BRIDGE_PROGRAM_ID"])

        # Get function name of the qualifications lambda for storing and retrieving
        self.qualifications_lambda: str = os.environ["QUALIFICATIONS_LAMBDA"]

        # Initialize the program
        self.program: Program = Program(id=self.program_id)

        # Create a lambda client
        self.lambda_client = boto3.client('lambda')


    def handle_event(self, event, context):

        try:
            # Get all of the courses in the program
            self.program.get_courses(self.bridge_url, self.bridge_auth_token)

            # Dictionary to store all completed courses for users
            learners: dict[str, Learner] = {}

            # Timestamp to restrict course enrollment results
            base_time: str = self.get_latest_update_time()

            # Get all "completed" enrollments for each course
            for course in self.program.courses:
                course.get_completed_enrollments(
                        self.bridge_url, self.bridge_auth_token,
                        base_time, learners
                )

            # Learner class stores a reference to the learner with the latest
            # last_updated value. Add this learner or update the existing one
            # depending on if the stored user_id is in learners or not.
            latest_learner: Learner = Learner._latest_timestamp_learner
            
            # If latest_learner is None, this means there were no users
            # returned from the data at all (should happen only for all new
            # courses with no users enrolled at all). Return success early
            if type(latest_learner) is type(None):
                return buildResponse(statusCode = 200, body = {})

            if latest_learner.user_id not in learners:
                learners[latest_learner.user_id] = latest_learner

            else:
                learners[latest_learner.user_id].update_timestamp(latest_learner.last_updated)


            # Send patch request to the backend api to update each user's qualifications
            for user_id in learners:
                learner = learners[user_id]
                status, response = self.patch_learner_aws(
                        learner
                )

                """
                Patch returning 400 means the user hasn't been created for qualifications
                yet. Post the enrollments instead to add the user to the qualifications.
                """
                if status == 400:
                    self.post_learner_aws(learner)

            response = buildResponse(statusCode = 200, body = {})

        except Exception as e:
            errorMsg: str = f"We're sorry, but something happened. Try again later."
            body = { 'errorMsg': errorMsg }
            response = buildResponse(statusCode = 500, body = body)

        return response

    def send_event_to_lambda(self, target_lambda: str, event: dict) -> dict:
        """
        Sends an event to a lambda function.

        :params target_lambda: The name of the lambda function to send the event to.
        :params event: The event to send.
        :returns: Response dictionary from the lambda function.
        """

        try:
            content: dict = self.lambda_client.invoke(
                FunctionName=target_lambda,
                Payload=json.dumps(event)
            )
        except Exception as e:
            raise Exception(e)

        response = json.loads(content['Payload'].read())
        return response


    def separate_enrollments(self, enrollments: list[CompletableItem]) -> list[tuple[str, list[dict]]]:
        """
        Separates enrollments into lists based on keywords in the course names.

        :params enrollments: The list of enrollments to separate.
        :returns: A list of tuples where the first item is the key word to use
                  when storing in a dictionary, and the second item is the
                  list of enrollments relating to the key word.
        """

        # Prepare all lists to separate enrollments into
        lists: dict = {
            "trainings": [],
            "waivers": [],
            "miscellaneous": [],
        }

        # Separate enrollments into respective lists
        for enrollment in enrollments:
            item = {
                "name": enrollment.name,
                "completion_status": enrollment.completion_status
            }

            # Append to waivers if "waiver" contained in the enrollment name
            if "waiver" in enrollment.name.lower():
                lists["waivers"].append(item)

            # Append to trainings if "training" contained in the enrollment name
            elif "training" in enrollment.name.lower():
                lists["trainings"].append(item)

            # Otherwise add it to the "miscellaneous" list
            else:
                lists["miscellaneous"].append(item)

        return [(key, value) for key, value in lists.items()]


    def create_qualifications_patch_body(self, learner: Learner) -> dict:
        """
        Returns a json object to use in a qualifications patch
        request based on the given learner.

        :params learner: The learner to use when creating the qualifications
                         patch request body.
        """

        # Separate the learner's enrollments
        enrollments: list[CompletableItem] = learner.enrolled_course_statuses
        separated_enrollments: list[tuple] = self.separate_enrollments(enrollments)

        # Create request_body
        request_body: dict = {}

        # Add each set from the separated enrollments
        for key, completeable_items in separated_enrollments:
            request_body[key] = completeable_items

        # Add the latest timestamp the user had changes for
        request_body["last_updated"] = learner.last_updated

        # Patch only needs the separated enrollments and last_updated timestamp, so just return
        return request_body


    def create_qualifications_post_body(self, learner: Learner) -> dict:
        """
        Returns a json object to use in a qualifications post
        request based on the given learner.

        :params learner: The learner to use when creating the qualifications
                         post request body.
        """

        # Separate the learner's enrollments
        enrollments: list[CompletableItem] = learner.enrolled_course_statuses
        separated_enrollments: list[tuple] = self.separate_enrollments(enrollments)

        # Create request_body
        request_body: dict = {}

        # Add each set from the separated enrollments
        for key, completeable_items in separated_enrollments:
            request_body[key] = completeable_items

        # Add the latest timestamp the user had changes for
        request_body["last_updated"] = learner.last_updated

        # Add the learner's user_id to the request body for post
        request_body["user_id"] = learner.user_id

        # Return the request body
        return request_body


    def patch_learner_aws(self, learner: Learner) -> tuple[int, dict]:
        """
        Sends a patch request event to the qualifications handler to update
        a learner's completed courses.

        :params learner: The learner to update.
        :returns: (statusCode, response_body)
        """

        # Create the qualifications patch request body
        request_body: dict = self.create_qualifications_patch_body(learner)

        # Create an event for the qualifications handler
        event: dict = create_rest_http_event(
            "PATCH",
            resource="/qualifications",
            body=request_body
        )

        # Send event to qualifications handler
        response = self.send_event_to_lambda(self.qualifications_lambda, event)

        # Extract the response body
        data: dict = json.loads(response['body'])

        # Get response body, if one exists
        response_body = data

        return (response['statusCode'], response_body)


    def post_learner_aws(self, learner: Learner) -> tuple[int, dict]:
        """
        Sends a post request event to the qualifications handler. Used
        to add new learners to the system.

        :params learner: The learner to add.
        :returns: (statusCode, response_body)
        """

        # Create the qualifications post request body
        request_body: dict = self.create_qualifications_post_body(learner)

        # Create an event for the qualifications handler
        event: dict = create_rest_http_event(
            "POST",
            resource="/qualifications",
            body=request_body
        )

        # Send event to qualifications handler
        response = self.send_event_to_lambda(self.qualifications_lambda, event)

        # Extract the response body
        data: dict = json.loads(response['body'])

        # Get response body, if one exists
        response_body = data

        return (response['statusCode'], response_body)


    def get_latest_update_time(self) -> str:
        """
        Gets the latest update time from the backend api qualifications.

        :returns: The latest update time from qualifications in the backend database.
        """

        # Prepare the query parameters
        queryStringParamters: dict = { 'limit': 1 }

        # Create an event for the qualifications handler
        event: dict = create_rest_http_event(
            "GET",
            resource="/qualifications",
            queryStringParameters=queryStringParamters
        )

        # Send event to qualifications handler
        response = self.send_event_to_lambda(self.qualifications_lambda, event)

        # Extract the last_updated time stamp
        data: dict = json.loads(response['body'])
        
        # In case the qualifications table is empty, use datetime.min as last_updated
        if len(data['qualifications']) == 0:
            last_updated: str = datetime.min.isoformat(timespec="seconds")
        else:
            last_updated: str = data['qualifications'][0]['last_updated']

        # Convert it to a valid bridge timestamp (BRIDGE_TIMESTAMP_FORMAT + TZ_OFFSET)
        updated_datetime = datetime.fromisoformat(last_updated)
        bridge_timestamp = updated_datetime.strftime(BRIDGE_TIMESTAMP_FORMAT)

        # Remove the last 3 of 6 seconds decimal places to convert to milliseconds
        bridge_timestamp = bridge_timestamp[0:-3]

        # Add TZ_OFFSET
        bridge_timestamp = bridge_timestamp + TZ_OFFSET

        # Return the timestamp
        return bridge_timestamp


def handler(event, context):
    # Pull qualification data from the Makerspace's Tiger Training program,
    # and POST it to the backend api.
    tiger_training_handler = TigerTrainingHandler()
    return tiger_training_handler.handle_event(event, context)
