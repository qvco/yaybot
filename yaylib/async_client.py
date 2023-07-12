"""
MIT License

Copyright (c) 2023-present Qvco, Konn

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import asyncio
import os
import time
import logging

from json import JSONDecodeError

import httpx
from cryptography.fernet import Fernet

from .api import API
from .asynchronous.call import *
from .asynchronous.cassandra import *
from .asynchronous.chat import *
from .asynchronous.group import *
from .asynchronous.login import *
from .asynchronous.misc import *
from .asynchronous.post import *
from .asynchronous.review import *
from .asynchronous.thread import *
from .asynchronous.user import *

from .config import ErrorType, ErrorMessage
from .errors import (
    HTTPError,
    BadRequestError,
    AuthenticationError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    YayServerError,
)
from .utils import Configs, generate_uuid


current_path = os.path.abspath(os.getcwd())


class AsyncBaseClient(API):
    pass


class AsyncClient(AsyncBaseClient):
    pass
