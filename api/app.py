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