#!/usr/bin/env python3
""" flask app """
from flask import Flask, jsonify
from auth import Auth

AUTH = Auth()

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """ GET /
    Return:
      - the status of the API
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['GET'], strict_slashes=False)
def users(email: str, password: str) -> str:
    """ GET /users
    Return:
      - the status of the API
    """
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "User created"})
    except ValueError:
        return jsonify({"message": "User already exists"})


@app.route('/sessions', methods=['GET'], strict_slashes=False)
def sessions(email: str, password: str) -> str:
    """ GET /sessions
    Return:
      - the status of the API
    """
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        return jsonify({"email": email, "message": "Session created"})
    else:
        return jsonify({"message": "Wrong password"})


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def sessions_delete(user_id: int) -> str:
    """ DELETE /sessions
    Return:
      - the status of the API
    """
    AUTH.destroy_session(user_id)
    return jsonify({"message": "Session deleted"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
