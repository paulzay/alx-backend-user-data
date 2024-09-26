#!/usr/bin/env python3
"""Auth module
"""
import bcrypt
from db import DB
import uuid


def _hash_password(password: str) -> str:
    """Hash password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def _generate_uuid() -> str:
    """Generate a UUID
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        """ initialize db"""
        self._db = DB()

    def register_user(self, email: str, password: str):
        """Register a user
        """
        user = self._db.find_user_by(email=email)
        if user is not None:
            raise ValueError('User emsil already exists')
        else:
            return self._db.add_user(email=email, hashed_password=password)

    def valid_login(self, email: str, password: str) -> bool:
        """Validate login
        """
        user = self._db.find_user_by(email=email)
        if user is None:
            return False
        return bcrypt.checkpw(password.encode(), user.hashed_password)

    def create_session(self, email: str) -> str:
        """Create a session
        """
        user = self._db.find_user_by(email=email)
        session_id = bcrypt.gensalt()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> str:
        """Get user from session id
        """
        if session_id is None:
            return
        user = self._db.find_user_by(session_id=session_id)
        if user is None:
            return
        return user.email

    def destroy_session(self, user_id: int):
        """Destroy a session
        """
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """Get reset password token
        """
        user = self._db.find_user_by(email=email)
        token = bcrypt
        self._db.update_user(user.id, reset_token=token)
        return token

    def update_password(self, email: str, reset_token: str, new_password: str):
        """Update password
        """
        user = self._db.find_user_by(email=email)
        if user.reset_token is None:
            raise ValueError
        if not bcrypt.checkpw(reset_token.encode(), user.reset_token):
            raise ValueError
        self._db.update_user(user.id, hashed_password=new_password,
                             reset_token=None)
        return None
