from flask import Flask
from flask import request
import requests

app = Flask(__name__)


# CREATE TASK
@app.route("/tasks/create")
def create_task():
    """
        Creates a new task in the database

        ================   ============
        **Endpoint**        /api/tasks/create
        **Request Type**    POST
        **Access**          ALL
        ================   ============


        Parameters
        -----------
        task_name: str, required
            The name of the task to be added.
        description : str, required
            The description of the task to be added.
        frequency: str, required
            The frequency of the task to be added.
        machine_id : str, required
            The machine id of the task to be added.
        machine_name : str, required
            The machine name on which the task to be added will be performed.
        completion_date : datetime, required
            The completion date of the task to be added.
        start_date: datetime, required
            The start date of the task to be added.

        Returns
        --------

        """
    task_name = request.args.get('TaskName')
    description = request.args.get('Description')
    frequency = request.args.get('Frequency')
    machine_id = request.args.get('MachineId')
    machine_name = request.args.get('MachineName')
    completion_time = request.args.get('CompletionTime')
    start_date = request.args.get('StartDate')

    payload = {'TaskName': task_name, 'Description': description, 'Frequency': frequency, 'MachineId': machine_id,
               'MachineName': machine_name, 'CompletionTime': completion_time, 'StartDate': start_date}

    response = requests.get(
        "https://iilws7onba.execute-api.us-east-1.amazonaws.com/prod",
        params=payload)
    return response.text


# EDIT TASK
@app.route("/tasks/edit")
def edit_task():
    parent_id = request.args.get('ParentId')
    task_name = request.args.get('TaskName')
    description = request.args.get('Description')
    frequency = request.args.get('Frequency')
    machine_id = request.args.get('MachineId')
    completion_time = request.args.get('CompletionTime')

    payload = {'TaskName': task_name, 'Description': description, 'Frequency': frequency, 'MachineId': machine_id,
               'CompletionTime': completion_time, 'ParentId': parent_id}
    response = requests.get(
        "https://imxhdniv4b.execute-api.us-east-1.amazonaws.com/prod",
        params=payload)
    return response.text

# DELETE TASK


@app.route("/tasks/delete")
def delete_task():
    parent_id = request.args.get('ParentId')

    payload = {'ParentId': parent_id}

    response = requests.get(
        "https://lkohfoidbc.execute-api.us-east-1.amazonaws.com/prod",
        params=payload)
    return response.text

# VIEW TASK


@app.route("/tasks/view")
def view_task():
    parent_id = request.args.get('ParentId')
    due_date = request.args.get('DueDate')

    payload = {'ParentId': parent_id, 'DueDate': due_date}
    response = requests.get(
        "https://i7z47ol3l4.execute-api.us-east-1.amazonaws.com/prod",
        params=payload)
    return response.text


# VIEW UPCOMING TASKS
@app.route("/tasks/upcoming")
def view_upcoming_tasks():
    days_forward = request.args.get('DaysForward')

    payload = {'DaysForward': days_forward}
    response = requests.get(
        "https://72aw5tpqba.execute-api.us-east-1.amazonaws.com/prod",
        params=payload)
    return response.text


# COMPLETE TASK
@app.route("/tasks/complete")
def complete_task():
    due_date = request.args.get('DueDate')
    parent_id = request.args.get('ParentId')
    completed_by = request.args.get('CompletedBy')

    payload = {
        'DueDate': due_date,
        'ParentId': parent_id,
        'CompletedBy': completed_by}

    response = requests.get(
        "https://uev3a2amyh.execute-api.us-east-1.amazonaws.com/prod",
        params=payload)
    return response.text
