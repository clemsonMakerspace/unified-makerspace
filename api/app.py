from flask import Flask

app = Flask(__name__)


# Lambda Application Endpoint (AWSEdcuate): https://72aw5tpqba.execute-api.us-east-1.amazonaws.com/prod
# Lambda Application Endpoint (MakerSpace): https://9mgegu2fge.execute-api.us-east-1.amazonaws.com/prod


# GET TASKS
@app.route("/tasks")
def get_tasks():
    return 200


def query_tasks(year, dynamodb=None):
    pass


# GET TASK REQUESTS
@app.route("/requests")
def get_task_requests():
    return 200


# GET NUMBER OF USERS
@app.route("/num_users")
def get_num_users():
    return 200


# GET NUMBER OF NEW USERS
@app.route("/num_new_users")
def get_num_new_users():
    return 200


# GET TASK INFO BY ID
@app.route("/task/<id>")
def get_task_info(id):
    return 200


# GET USER INFO BY PK
@app.route("/user/<pk>")
def get_user_info(pk):
    return 200


# GET MACHINES LIST BY TYPE
@app.route("machine/<type>")
def get_machines(type):
    return 200
