"""
app.py

Simple example server for the Makerspace
website. The purpose is two-fold: to provide
mock data for the site and to test if requests
are valid.

Note
-----
For development, the default test server is
'http://localhost:5000'. This can be configured
in Angular's `environment` settings.

"""
import os
import sys

import dotenv
from base64 import b64encode
from flask import Flask, session, request
from flask_cors import CORS

from utils import fetch_data
from utils import fetch_response

# to enable importing of distant modules
sys.path.append("../../api")

# load environment vars
dotenv.load_dotenv()

# flask configuration
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = b64encode(os.urandom(16)).decode('utf-8')
auth_token = app.config['SECRET_KEY']

# load users before start
users = fetch_data('users')


"""
Admin
"""



@app.route('/api/admin', methods=['POST'])
def generate_user_token():
    # implemented
    return dict(code=200, user_token=app.config['SECRET_KEY'])



@app.route('/api/admin', methods=['PATCH'])
def reset_password():
    return dict(code=200, message="Password reset email sent.")

"""
Users
"""
#
# @app.route('/api/users', methods=['POST'])
# def change_password():
#     if 'new_password' in request.form:
#         return login()
#     return dict(code=200, message="Password changed successfully.")
#

@app.route('/api/users', methods=['PUT'])
def create_user():
    return dict(code=200, user=users[0], auth_token=auth_token)


@app.route('/api/users', methods=['DELETE'])
def delete_user():
    return dict(code=200, message="User has been successfully deleted.")


@app.route('/api/users', methods=['GET'])
def get_users():
    return dict(code=200, users=users)


@app.route('/api/users', methods=['POST'])
def login():
    return dict(code=200, user=users[0], auth_token=auth_token)


@app.route('/api/users', methods=['PATCH'])
def update_user():
    return dict(code=200, message="User has been updated.")


"""
Tasks
"""

@app.route('/api/tasks', methods=['POST'])
def create_task():
    return dict(code=200, task_id="RANDOM_TASK_ID")


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return dict(code=200, tasks=fetch_data('tasks'))


@app.route('/api/tasks', methods=['DELETE'])
def resolve_task():
    return dict(code=200, message="Resolved task successfully.")


@app.route('/api/tasks', methods=['UPDATE'])
def update_task():
    return dict(code=200, message="Task updated successfully.")


"""
Machines
"""

@app.route('/api/machines', methods=['DELETE'])
def delete_machine():
    return dict(code=200, message="Machine deleted successfully.")


@app.route('/api/machines', methods=['POST'])
def get_machines_status():
    return dict(code=200, machines=fetch_response('machines'))


"""
Visitors
"""

@app.route('/api/visitors', methods=['PUT'])
def create_visitor():
    return dict(code=200, message="Visitor successfully created.")


@app.route('/api/visitors', methods=['POST'])
def get_visitors():
    return dict(code=200, visitors=fetch_data('visits'))



@app.route('/api/visitors', methods=['GET'])
def get_visitor_data():
    visitors = fetch_data('visitors')
    for visitor in visitors:
        if request.args.get('visitor_id') == visitor['visitor_id']:
            return dict(code=200, visitor=visitor)




