#!/usr/bin/env python3
"""
Basic Auth class definition
"""

from api.v1.auth import Auth
import base64
import re
from typing import TypeVar


class BasicAuth(Auth):
    """
    class definition for Baic Auth
    """
