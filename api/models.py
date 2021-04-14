"""
These are the various objects, or "models" that the api uses. Each class
should be represented as a javascript object, with the parameters as keys.
"""

from attr import dataclass


@dataclass
class Task:
    """
    Represents a task object. `status` must be either be 2 (Completed), 1 (In-Progress),
    or 0 (Not Started). `task_name` is a brief description of the task. `assigned_to`
    is the user_id of the user to who the task is assigned to. `tags` are a list of
    strings associated with the task (e.g. metadata). The first tag is the machine name
    or '*' if the task is not associated with any particular machine.

    Note
    -----
    Tags are not case-sensitive.

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
class Resource:
    """
    Represents a resource. Currently valid resource names are
    "tasks", "visitors", "machines", and "administrative".
    """
    resource_id: str
    resource_name: str
    can_read: bool
    can_delete: bool
    can_write: bool


@dataclass
class Permission:
    """
    Represents rules regarding resources. Each user is associated
    with zero or more permissions, which specify access control for
    one or more resources. If a user does not have a certain
    permission, access is denied.
    """
    policy_id: str
    policy_name: str
    access: [Resource]


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


@dataclass
class Visitor:
    """
    Represents a visitor to the MakerSpace.
    """
    hardware_id: str
    college: str
    degree_type: str
    first_name: str
    last_name: str
    major: str
    visitor_id: str



@dataclass
class Visit:
    """
    Represents a visit to the MakerSpace, and whether
    it is the first visit.
    """
    visit_id: str
    visitor_id: str
    date_visited: int
    first_visit: bool


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

    Note:
    ------
    Depending on the implementation, this amy not be needed.
    """
    machine_name: str
    machine_state: int
