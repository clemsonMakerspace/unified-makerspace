"""
These are the various objects, or "models" that will be exchanged
with the api. Each class should be represented as a javascript object,
with the parameters as keys.
"""

from attr import dataclass


class Task(object):
    pass


@dataclass()
class Maintainer:
    """
    Model for a person who can be assigned tasks.
    """
    name: str
    assigned_tasks: [Task]


@dataclass()
class Task:
    """
    Model for task object. `status` must be either "Completed", "In-Progress",
    or "Not Started".
    """

    task_id: str
    tags: [str]
    description: str
    assigned_to: Maintainer
    status: str


@dataclass()
class Visitor:
    """
    Represents a visitor to the MakerSpace.
    """
    date_visited: str
    is_new: bool


@dataclass()
class Request:
    """
    Represents a user request to the MakerSpace staff. `request_id`
    is not passed in when creating requests.
    """
    requester_name: str
    description: str
    request_id: str
