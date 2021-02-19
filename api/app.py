from flask import Flask

app = Flask(__name__)


@app.route('/')
def get_tasks():
    return "hello"


@app.route('/test')
def get_more_tasks():
    return "world"
