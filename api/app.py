from flask import Flask
from flask import request
import requests

app = Flask(__name__)

# Lambda Application Endpoint (AWSEdcuate): https://72aw5tpqba.execute-api.us-east-1.amazonaws.com/prod
# Lambda Application Endpoint (MakerSpace): https://9mgegu2fge.execute-api.us-east-1.amazonaws.com/prod

makerspace_endpoint = "https://9mgegu2fge.execute-api.us-east-1.amazonaws.com/prod"
# GET TASKS
@app.route("/tasks")
def get_tasks():
    payload= {'DaysForward':'1'}
    response = requests.get(makerspace_endpoint,params=payload)
    print(response.json())
    return response.json()

#def query_tasks(year, dynamodb  =None):


# GET TASK REQUESTS
@app.route("/requests")
def get_task_requests():
    return '200'

# GET NUMBER OF USERS
@app.route("/num_users")
def get_num_users():
    return '200'

# GET NUMBER OF NEW USERS
@app.route("/num_new_users")
def get_num_new_users():
    return '200'


# GET TASK INFO BY ID
@app.route("/task/<id>")
def get_task_info(id):
    return '200'

# GET USER INFO BY PK
@app.route("/user/<pk>")
def get_user_info(pk):
    return '200'

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
    pass

# MAINTAIN TASKS
@app.route("/maintainTasks")
def maintain_tasks():
    pass

# EDIT TASK
@app.route("/editTask")
def edit_task():
    pass

# DELETE TASK
@app.route("/deleteTask")
def delete_task():
    pass

# VIEW TASK
@app.route("/viewTask")
def view_task():
    pass


# VIEW UPCOMING TASKS
@app.route("/viewUpcomingTasks")
def view_upcoming_tasks():
    pass


# COMPLETE TASK
@app.route("/completeTask")
def complete_task():
    pass