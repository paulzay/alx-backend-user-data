#!/usr/bin/env python3
""" Module of SessionAuth views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv
from api.v1.auth.session_auth import SessionAuth

sa = SessionAuth()


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ POST /api/v1/auth_session/login
    JSON body:
      - email
      - password
    Return:
      - User object JSON represented
      - 400 if email or password is missing
      - 401 if email or password is wrong
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or password is None:
        return jsonify({"error": "email or password missing"}), 400
    user = User.search({'email': email})
    if user is None or not user[0].is_valid_password(password):
        return jsonify({"error": "no user found with this email/password"}), 401
    from api.v1.app import auth
    session_id = sa.create_session(user[0].id)
    user_dict = jsonify(user[0].to_json())
    user_dict.set_cookie(getenv('SESSION_NAME'), session_id)
    return user_dict


@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """ DELETE /api/v1/auth_session/logout
    Return:
      - empty JSON
    """
    if sa.destroy_session(request):
        return jsonify({}), 200
    abort(404)
  

@app_views.route('/auth_session/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """ GET /api/v1/auth_session/profile
    Return:
      - User object JSON represented
      - 404 if no user is authenticated
    """
    user = sa.current_user(request)
    if user is None:
        abort(404)
    return jsonify(user.to_json())
