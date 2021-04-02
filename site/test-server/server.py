

from models import User
from flask import Flask
app = Flask()

# todo add auth tokens


@app.route('/api/users', methods=['POST'])
def create_user():
    return User()
