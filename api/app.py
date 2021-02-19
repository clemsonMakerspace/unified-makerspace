from flask import Flask

app = Flask(__name__)




@app.route("/tasks")
def get_tasks():
    return 200

@app.route("/requests")
def get_task_requests():
    return 200

@app.route("/num_users")
def get_num_users():
    return 200

@app.route("/num_new_users")
def get_num_new_users():
    return 200

@app.route("/task/<id>")
def get_task_info(id):
    return 200

@app.route("/user/<pk>")
def get_user_info(pk):
    return 200

@app.route("machine/<type>")
def get_machines(type):
    return 200

