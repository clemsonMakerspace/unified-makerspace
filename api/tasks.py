from flask import Flask
from flask import request
import requests

app = Flask(__name__)



# CREATE TASK
@app.route("/task/create")
def create_task():
    task_name = request.args.get('TaskName')
    description = request.args.get('Description')
    frequency = request.args.get('Frequency')
    machine_id = request.args.get('MachineId')
    machine_name = request.args.get('MachineName')
    completion_time = request.args.get('CompletionTime')
    start_date = request.args.get('StartDate')

    payload = { 'TaskName' : task_name, 'Description': description, 'Frequency' : frequency, 'MachineId' : machine_id,
                'MachineName' : machine_name, 'CompletionTime' : completion_time, 'StartDate': start_date }

    response = requests.get("https://iilws7onba.execute-api.us-east-1.amazonaws.com/prod",params=payload)
    return response.text


# EDIT TASK
@app.route("/task/edit")
def edit_task():
    parent_id = request.args.get('ParentId')
    task_name = request.args.get('TaskName')
    description = request.args.get('Description')
    frequency = request.args.get('Frequency')
    machine_id = request.args.get('MachineId')
    completion_time = request.args.get('CompletionTime')

    payload = {'TaskName': task_name, 'Description': description, 'Frequency': frequency, 'MachineId': machine_id,
                'CompletionTime': completion_time, 'ParentId': parent_id }
    response = requests.get("https://imxhdniv4b.execute-api.us-east-1.amazonaws.com/prod",params=payload)
    return response.text

# DELETE TASK
@app.route("/task/delete")
def delete_task():
    parent_id = request.args.get('ParentId')

    payload ={'ParentId': parent_id }

    response = requests.get("https://lkohfoidbc.execute-api.us-east-1.amazonaws.com/prod", params=payload)
    return response.text

# VIEW TASK
@app.route("/task/view")
def view_task():
    parent_id = request.args.get('ParentId')
    due_date = request.args.get('DueDate')

    payload = {'ParentId' : parent_id, 'DueDate' : due_date }
    response = requests.get("https://i7z47ol3l4.execute-api.us-east-1.amazonaws.com/prod", params=payload)
    return response.text


# VIEW UPCOMING TASKS
@app.route("/task/upcoming")
def view_upcoming_tasks():
    days_forward = request.args.get('DaysForward')

    payload = {'DaysForward': days_forward }
    response = requests.get("https://72aw5tpqba.execute-api.us-east-1.amazonaws.com/prod",params=payload)
    return response.text


# COMPLETE TASK
@app.route("/task/complete")
def complete_task():
    due_date = request.args.get('DueDate')
    parent_id = request.args.get('ParentId')
    completed_by = request.args.get('CompletedBy')

    payload = {'DueDate': due_date, 'ParentId': parent_id, 'CompletedBy': completed_by }

    response = requests.get("https://uev3a2amyh.execute-api.us-east-1.amazonaws.com/prod",params=payload)
    return response.text