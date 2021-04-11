"""
app.py

Simple example server for the MakerSpace
website.

Note
-----
For development, the default test server is
'http://localhost:4000'. This can be configured
in Angular's `environment` settings.

"""
import os
import sys

import yaml
from flask import Flask, session, request
from flask_cors import CORS

# to enable importing of distant module
sys.path.append("../../api")
from models import User, Task, Visitor, Machine, Permission, Visit

# todo spread this out?

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = "TEST_KEY"


# todo add auth tokens (?)
# todo dict within a dict

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


def fetch_response(resource: str, data_path= './responses'):
    """
    Gets pre-calculated responses.
    """
    path = os.path.join(data_path, f"{resource}.yaml")
    with open(path) as f:
        data = yaml.load(f)
    return data



# load users on start
# todo session?
users = fetch_data('users')
auth_token = "TEST_TOKEN"

"""
Endpoints
"""


# todo return auth token
@app.route('/api/users', methods=['POST'])
def login():
    return dict(code=200, user=users[0], auth_token=auth_token)


@app.route('/api/users', methods=['PUT'])
def create_user():
    return dict(code=200, user=users[0])


@app.route('/api/users', methods=['DELETE'])
def delete_user():
    return dict(code=200, message="User has been successfully deleted.")


@app.route('/api/users', methods=['GET'])
def get_users():
    return dict(code=200, users=users)


# todo implement
@app.route('/api/users', methods=['PATCH'])
def update_user():
    for i, user in enumerate(session["users"]):
        if request.json.user_id == user.user_id:
            session['users'][i] = User(**request.json)
    return dict(code=200, message="User has been updated.")


# todo get tasks for user...?

# tasks
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    if not 'tasks' in session:
        session['tasks'] = fetch_data('tasks')
        session.modified = True
    return dict(code=200, tasks=session['tasks'])


# todo implement
@app.route('/api/tasks', methods=['POST'])
def create_task():
    pass


# todo fix
@app.route('/api/tasks', methods=['DELETE'])
def resolve_task():
    tasks = session['tasks']
    # list(filter(lambda t: t.task_id == request.json['task_id'], tasks))
    return dict(code=200, message="Task Resolved.")


# todo implement
# todo also implement on front-end
@app.route('/api/tasks', methods=['UPDATE'])
def update_task():
    for i, task in enumerate(session['tasks']):
        if request.json.task_id == task.task_id:
            session['tasks'][i] = Task(**request.json)
    return dict(code=200, message="Tasks updated.")


# machines
@app.route('/api/machines', methods=['POST'])
def get_machines_status():
    return dict(code=200, machines=fetch_response('machines'))


# visitors
@app.route('/api/visitors', methods=['POST'])
def get_visitors():
    return dict(code=200, visitors=fetch_response('visits'))

# todo add main clause
