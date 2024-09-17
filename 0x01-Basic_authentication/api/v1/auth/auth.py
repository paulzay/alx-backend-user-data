#!/usr/bin/env python3
""" auth class """
from typing import TypeVar, List
from flask import request


class Auth:
    """ class definition"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require suth method """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        
        if path in excluded_paths:
            return False

    def authorization_header(self, request=None) -> str:
        """ auth hesder method"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ current user method """
        return None
