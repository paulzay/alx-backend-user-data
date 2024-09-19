#!/usr/bin/env python3
""" auth class """
from typing import TypeVar, List
from flask import request
import os


class Auth:
    """ class definition"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require suth method """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path += '/'
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """ auth hesder method"""
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """ current user method """
        return None

    def session_cookie(self, request=None):
        """ Session cookie method
        """
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name)
