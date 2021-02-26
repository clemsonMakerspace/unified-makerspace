from flask import Flask
from flask import request
import requests

app = Flask(__name__)

# Lambda Application Endpoint (AWSEdcuate): https://72aw5tpqba.execute-api.us-east-1.amazonaws.com/prod
# Lambda Application Endpoint (MakerSpace): https://9mgegu2fge.execute-api.us-east-1.amazonaws.com/prod

makerspace_endpoint = "https://9mgegu2fge.execute-api.us-east-1.amazonaws.com/prod"


# VIEW MACHINE BY ID
@app.route("/viewMachine")
def get_machines():
    machine_id = request.args.get('machine_id')
    payload = {'machine_id': machine_id }
    response = requests.get("https://m0g7r8hjsk.execute-api.us-east-1.amazonaws.com/prod",params=payload)
    return response.text


# ADD MACHINE BY URL QUERY PARAMS
@app.route("/addMachine")
def add_machine():
    machine_id = request.args.get('machine_id')
    machine_type = request.args.get('machine_type')
    machine_name = request.args.get('machine_name')
    payload = { 'machine_id': machine_id, 'machine_type': machine_type, 'machine_name': machine_name}
    response = requests.get("https://28igyfdybf.execute-api.us-east-1.amazonaws.com/prod",params=payload)
    return response.text

# VIEW MACHINE BY TYPE
@app.route("/viewMachineByType")
def view_machine_by_type():
    machine_type = request.args.get('machine_type')
    payload = {'machine_type': machine_type }
    response = requests.get("https://yxnx3ps6ai.execute-api.us-east-1.amazonaws.com/prod",params=payload)
    return response.text

# VIEW MACHINE HISTORY
@app.route("/viewMachineHistory")
def view_machine_history():
    machine_id = request.args.get('MachineId')
    days_back = request.args.get('DaysBack')
    payload = { 'MachineId': machine_id, 'DaysBack': days_back }
    response = requests.get("https://kbh1vbi02h.execute-api.us-east-1.amazonaws.com/prod", params=payload)
    return response.text

# EXPORT MACHINE HISTORY
@app.route("/exportMachineHistory")
def export_machine_history():
    machine_id = request.args.get('MachineId')
    days_back = request.args.get('DaysBack')
    payload = {'MachineId': machine_id, 'DaysBack': days_back}
    response = requests.get("https://8jhka7ee33.execute-api.us-east-1.amazonaws.com/prod", params=payload)
    return response.text

# VIEW MACHINE UPCOMING TASKS
@app.route("/viewMachineUpcomingTasks")
def view_machine_upcoming_tasks():
    machine_id = request.args.get('MachineId')
    days_forward = request.args.get('DaysForward')
    payload = {'MachineId' : machine_id, 'DaysForward': days_forward }
    response = requests.get("https://b50w8zo4ji.execute-api.us-east-1.amazonaws.com/prod", params=payload)
    return response.text

# DELETE MACHINE TYPE
@app.route("/deleteMachineType")
def delete_machine_type():
    machine_type = request.args.get('machine_type')
    payload = { 'machine_type' : machine_type }
    response = requests.get("https://ks3lf0h05j.execute-api.us-east-1.amazonaws.com/prod", params=payload)
    return response.text

# EDIT MACHINE NAME
@app.route("/editMachineName")
def edit_machine_name():
    machine_id = request.args.get('machine_id')
    new_name = request.args.get('new_name')
    payload = { 'machine_id' : machine_id, 'new_name' : new_name }
    response = requests.get("https://yhva0or5h4.execute-api.us-east-1.amazonaws.com/prod", params=payload)
    return response.text

# DELETE MACHINE
@app.route("/deleteMachine")
def delete_machine():
    machine_id = request.args.get('machine_id')
    machine_type = request.args.get('machine_type')
    payload = {'machine_id' : machine_id , 'machine_type': machine_type }
    response = requests.get("https://3pbr1o7se2.execute-api.us-east-1.amazonaws.com/prod", params=payload)
    return response.text

# VIEW MACHINE TYPES
@app.route("/viewMachineTypes")
def view_machine_types():
    response = requests.get("https://bqlj5bqdkl.execute-api.us-east-1.amazonaws.com/prod")
    return response.text

# ADD MACHINE TYPE
@app.route("/addMachineType")
def add_machine_type():
    machine_type = request.args.get('machine_type')
    payload = { 'machine_type' : machine_type }
    response = requests.get("https://zl8rpx0i43.execute-api.us-east-1.amazonaws.com/prod", params=payload)
    return response.text

# VIEW PARENTS BY MACHINE
@app.route("/viewParentsByMachine")
def view_parents_by_machine():
    machine_id = request.args.get('MachineId')
    payload = {'MachineId' : machine_id }
    response = requests.get("https://fpzztw4zoe.execute-api.us-east-1.amazonaws.com/prod", params=payload)
    return response.text

# VIEW MACHINE BY TYPES
@app.route("/viewMachineByTypes")
def view_machine_by_types():
    machine_type = request.args.get('machine_type')
    payload = {'machine_type' : machine_type}
    response = requests.get("https://yxnx3ps6ai.execute-api.us-east-1.amazonaws.com/prod",params=payload)
    return response.text

# CREATE TASK
@app.route("/createTask")
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
@app.route("/editTask")
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
@app.route("/deleteTask")
def delete_task():
    parent_id = request.args.get('ParentId')

    payload ={'ParentId': parent_id }

    response = requests.get("https://lkohfoidbc.execute-api.us-east-1.amazonaws.com/prod", params=payload)
    return response.text

# VIEW TASK
@app.route("/viewTask")
def view_task():
    parent_id = request.args.get('ParentId')
    due_date = request.args.get('DueDate')

    payload = {'ParentId' : parent_id, 'DueDate' : due_date }
    response = requests.get("https://i7z47ol3l4.execute-api.us-east-1.amazonaws.com/prod", params=payload)
    return response.text


# VIEW UPCOMING TASKS
@app.route("/viewUpcomingTasks")
def view_upcoming_tasks():
    days_forward = request.args.get('DaysForward')

    payload = {'DaysForward': days_forward }
    response = requests.get("https://72aw5tpqba.execute-api.us-east-1.amazonaws.com/prod",params=payload)
    return response.text


# COMPLETE TASK
@app.route("/completeTask")
def complete_task():
    due_date = request.args.get('DueDate')
    parent_id = request.args.get('ParentId')
    completed_by = request.args.get('CompletedBy')

    payload = {'DueDate': due_date, 'ParentId': parent_id, 'CompletedBy': completed_by }

    response = requests.get("https://uev3a2amyh.execute-api.us-east-1.amazonaws.com/prod",params=payload)
    return response.text