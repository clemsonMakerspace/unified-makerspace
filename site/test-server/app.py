from flask import Flask

from models import User

app = Flask('__name__')

# todo add auth tokens
# todo implement


test_user = User(first_name='Joe', last_name='Goldberg',
                 user_id="342543", assigned_tasks=[],
                 permissions=[])

test_users = [test_user]




@app.route('/api/users', methods=['POST'])
def create_user():
    return dict(code=200, user=test_user, auth_token='')


@app.route('/api/users', methods=['DELETE'])
def delete_user():
    return dict(code=200, message="User has been successfully deleted." )


@app.route('/api/users', methods=['GET'])
def get_users():
    return dict(code=200, users=test_users)


@app.route('/api/users', methods=['GET'])
def update_permissions():
    pass

