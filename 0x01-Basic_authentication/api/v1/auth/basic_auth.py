#!/usr/bin/env python3
""" Basic Auth class"""
from api.v1.auth import Auth
import base64
import re
from typing import TypeVar


class BasicAuth(Auth):
    """ class definition for Baic Auth """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ extract header authorization"""
        if authorization_header is None or type(authorization_header
                                                ) is not str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """ decode authorization header """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        if not is_valid_base64(base64_authorization_header):
            return None
        return base64.decode(base64_authorization_header, 'utf-8')

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """ extract email and password from header"""
        if decoded_base64_authorization_header is None:
            return None
        if type(decoded_base64_authorization_header) is not str:
            return None
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ get user object from credentials"""
        pass

    def current_user(self, request=None) -> TypeVar('User'):
        """ get user object """
        pass


def is_valid_base64(s):
    """ valid base64 checker """
    pattern = r'^[A-Za-z0-9+/]*[=]{0,2}$'
    return bool(re.match(pattern, s)) and len(s) % 4 == 0
