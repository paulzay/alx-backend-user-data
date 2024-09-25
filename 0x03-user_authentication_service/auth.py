#!/usr/bin/env python3
"""Auth module
"""
import bcrypt
from db import DB


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()
    
    def register_user(self, email: str, password: str):
        user = self._db.find_user_by(email=email)
        if user is not None:
            raise ValueError('User emsil already exists')
        else:
          return self._db.add_user(email=email, hashed_password=password)

def _hash_password(password: str) -> str:
    """Hash password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
