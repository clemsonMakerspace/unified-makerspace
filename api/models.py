"""
These are the various objects, or "models" that the api uses. Each class
should be represented as a javascript object, with the parameters as keys.
Dates should be encoded in epoch time (milliseconds since the start of
January 1st, 1970).
"""

from attr import dataclass


# todo should assigned to be an id?
# todo get person by user id
# todo is task status ne

@dataclass
class Task:
    """
    Represents a task object. `status` must be either be 2 (Completed), 1 (In-Progress),
    or 0 (Not Started). `task_name` is a brief description of the task. `assigned_to`
    is the user_id of the user to who the task is assigned to. `tags` are a list of
    strings associated with the task (e.g. metadata). The first tag is the machine name
    or '*' if the task is not associated with any particular machine.
    """

    task_id: str
    task_name: str
    description: str
    assigned_to: str
    date_created: int
    date_resolved: int
    tags: [str]
    status: int


@dataclass
class Permission:
    """
    Represents a set of rules regarding a certain resource.
    """
    resource_id: str
    can_read: bool
    can_write: bool
    can_delete: bool


@dataclass
class User:
    """
    Represents a registered user of the MakerSpace. Users are
    those who will be using the dashboard (not visitors). `assigned_tasks`
    is a list of task_ids.
    """
    user_id: str
    first_name: str
    last_name: str
    assigned_tasks: [str]
    permissions: [Permission]


# todo fix this - no date visited and is_new?
@dataclass
class Visitor:
    """
    Represents a visitor to the MakerSpace. `visitor_information`
    includes first name, last name, and major.
    """
    visit_id: str
    date_visited: str
    is_new: bool
    visitor_info: dict


@dataclass
class Request:
    """
    Represents a maintenance request to the MakerSpace. `request_id`
    is not passed in when creating requests.
    """
    requester_name: str
    description: str
    request_id: str


@dataclass
class Machine:
    """
    Represents a machine. `machine_state` can be either "1" (Working) or
    "O" (Not Working).
    """
    machine_name: str
    machine_state: int