"""
These are the various objects, or "models" that the api uses. Each class
should be represented as a javascript object, with the parameters as keys.
Dates should be encoded in ISO 8601.
"""

from attr import dataclass


@dataclass()
class Task:
    """
    Represents a task object. `status` must be either "Completed", "In-Progress",
    or "Not Started". `assigned_to` is the user_id of the user to who the task
    is assigned to.
    """

    task_id: str
    tags: [str]
    description: str
    assigned_to: str
    status: str


@dataclass()
class Permission:
    """
    Represents a set of rules regarding a certain resource.
    """
    resource_id: str
    can_read: bool
    can_write: bool
    can_delete: bool


@dataclass()
class User:
    """
    Represents a registered user of the MakerSpace.
    """
    first_name: str
    last_name: str
    user_id: str
    assigned_tasks: [Task]
    permissions: [Permission]


@dataclass()
class Visitor:
    """
    Represents a visitor to the MakerSpace.
    """
    visit_id: str
    visitor_information: dict
    date_visited: str
    is_new: bool


@dataclass()
class Request:
    """
    Represents a maintenance request to the MakerSpace. `request_id`
    is not passed in when creating requests.
    """
    requester_name: str
    description: str
    request_id: str
