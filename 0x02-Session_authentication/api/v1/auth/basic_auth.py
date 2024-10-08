#!/usr/bin/env python3
""" basic auth class """
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User
import base64
import binascii
from flask import request


class BasicAuth(Auth):
    """ Basic Auth class """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ extract base64 auth header """
        if authorization_header is None or not isinstance(authorization_header,
                                                          str):
            return None
        if authorization_header[:6] != 'Basic ':
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """ decode base64 auth header """
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None
        try:
            return base64.b64decode(
                base64_authorization_header).decode('utf-8')
        except binascii.Error:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """ extract user credentials """
        if decoded_base64_authorization_header is None or not isinstance(
            decoded_base64_authorization_header, str) or \
           ':' not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ user object from credentials """
        if user_email is None or not isinstance(
            user_email, str) or user_pwd is None or not isinstance(
                user_pwd, str):
            return None
        try:
            user = User.search({'email': user_email})
        except Exception:
            return None
        if user is None or not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """ current user method """
        auth_header = self.authorization_header(request)
        base64_auth_header = self.extract_base64_authorization_header(
            auth_header)
        decoded_auth_header = self.decode_base64_authorization_header(
            base64_auth_header)
        user_creds = self.extract_user_credentials(decoded_auth_header)
        return self.user_object_from_credentials(user_creds[0], user_creds[1])

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ user object from credentials """
        if user_email is None or not isinstance(
            user_email, str) or user_pwd is None or not isinstance(
                user_pwd, str):
            return None
        try:
            user = User.search({'email': user_email})
        except Exception:
            return None
        if user is None or not user.is_valid_password(user_pwd):
            return None
        return user
