"""
utils.py

Utilities for loading data for the test server.

"""

from models import Visit
from models import Permission
from models import Machine
from models import Visitor
from models import Task
from models import User
import os
import sys
import yaml

# to enable importing of distant modules
sys.path.append("../../api")


def fetch_data(resource: str, data_path='./data') -> [dict]:
    """
    Load test data for `resource`. Data is instantiated as
    classes to ensure type safety. Simulates database.
    """

    # string to model mappings
    models = dict(tasks=Task, users=User, permissions=Permission,
                  visitors=Visitor, visits=Visit, machines=Machine)

    # invalid resource
    if resource not in models:
        return []

    # load from file
    path = os.path.join(data_path, f"{resource}.yaml")
    with open(path) as f:
        objs = []
        for obj in yaml.safe_load(f)[resource]:
            valid_obj = (models[resource])(**obj)
            objs.append(valid_obj.__dict__)

    return objs


def fetch_response(resource: str, data_path='./responses'):
    """
    Gets pre-calculated responses.
    """
    path = os.path.join(data_path, f"{resource}.yaml")
    with open(path) as f:
        data = yaml.safe_load(f)[resource]
    return data
