

from models import User
from flask import Flask


app = Flask('__name__')

# todo add auth tokens
# todo implement

test_user = User()



@app.route('/api/users', methods=['POST'])
def create_user():
    return dict(code=200, user=test_user, auth_token='')


@app.route('/api/users', methods=['DELETE'])
def delete_user():
    pass


@app.route('/api/users', methods=['GET'])
def get_users():
    pass


@app.route('/api/users', methods=['GET'])
def update_permissions():
    pass