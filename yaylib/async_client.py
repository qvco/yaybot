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

import os
import time
import logging

from json import JSONDecodeError

import httpx
from cryptography.fernet import Fernet

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


class AsyncBaseClient:
    """

    Base Client for AsyncClient.

    """

    def __init__(
        self,
        access_token: str = None,
        proxy: str = None,
        max_retries=3,
        backoff_factor=1.0,
        timeout=30,
        err_lang="ja",
        base_path=current_path + "/config/",
        loglevel_stream=logging.INFO,
        host=Configs.YAY_PRODUCTION_HOST,
    ):
        self.yaylib_version = Configs.YAYLIB_VERSION
        self.api_version = Configs.YAY_API_VERSION
        self.api_key = Configs.YAY_API_KEY
        self.secret_key = None

        self.proxy = {}
        if proxy is not None:
            self.proxy["https"] = proxy

        self.max_retries = max_retries
        self.retry_statuses = [500, 502, 503, 504]
        self.backoff_factor = backoff_factor
        self.timeout = timeout
        self.err_lang = err_lang
        self.base_path = base_path
        self.host = "https://" + host

        self._generate_all_uuids()
        self.session = httpx.AsyncClient(proxies=self.proxy, timeout=self.timeout)
        self.session.headers.update(Configs.REQUEST_HEADERS)
        self.session.headers.update({"X-Device-Uuid": self.device_uuid})
        if access_token:
            self.session.headers.setdefault("Authorization", f"Bearer {access_token}")

        self.logger = logging.getLogger("yaylib version: " + self.yaylib_version)

        if not os.path.exists(base_path):
            os.makedirs(base_path)

        ch = logging.StreamHandler()
        ch.setLevel(loglevel_stream)
        ch.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        handler_existed = False
        for handler in self.logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                handler_existed = True
                break
        if not handler_existed:
            self.logger.addHandler(ch)
        self.logger.setLevel(logging.DEBUG)

        self.logger.info("yaylib version: " + self.yaylib_version + " started")

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.session.aclose()

    async def _request(
        self, method, endpoint, params=None, payload=None, user_auth=True, headers=None
    ):
        headers = headers or self.session.headers

        if not user_auth:
            del headers["Authorization"]

        response = None
        backoff_duration = 0
        auth_retry_count = 0
        max_auth_retries = 2

        for i in range(self.max_retries):
            time.sleep(backoff_duration)

            self.logger.debug(
                "Making API request:\n\n"
                f"{method}: {endpoint}\n\n"
                f"Parameters: {params}\n\n"
                f"Headers: {headers}\n\n"
                f"Body: {payload}\n"
            )

            response = await self.session.request(
                method, endpoint, params=params, json=payload, headers=headers
            )

            if response.status_code == 401:
                if "/api/v1/oauth/token" in endpoint:
                    os.remove(self.base_path + "credentials.json")
                    message = "Refresh token expired. Try logging in again."
                    raise AuthenticationError(message)

                auth_retry_count += 1
                self.logger.debug("Access token expired. Refreshing tokens...")

                if auth_retry_count < max_auth_retries:
                    credentials = load_credentials(self)

                    if credentials is not None:
                        fernet = Fernet(self.secret_key)
                        credentials = decrypt(fernet, credentials)
                        refresh_token = credentials["refresh_token"]
                        response = await get_token(
                            self,
                            grant_type="refresh_token",
                            refresh_token=refresh_token,
                        )
                        save_credentials(
                            self,
                            fernet=fernet,
                            access_token=response.access_token,
                            refresh_token=response.refresh_token,
                            user_id=response.user_id,
                        )
                        self.session.headers[
                            "Authorization"
                        ] = f"Bearer {response.access_token}"
                        continue

                else:
                    os.remove(self.base_path + "credentials.json")
                    message = (
                        "Maximum authentication retries exceeded. Try logging in again."
                    )
                    raise AuthenticationError(message)

            if response.status_code not in self.retry_statuses:
                break

            if response is not None:
                self.logger.error(
                    f"Request failed with status code {response.status_code}. Retrying...",
                    exc_info=True,
                )
            else:
                self.logger.error("Request failed. Retrying...")

            backoff_duration = self.backoff_factor * (2**i)

        if response is None:
            return None

        self.logger.debug(
            "Received API response:\n\n"
            f"Status Code: {response.status_code}\n\n"
            f"Headers: {response.headers}\n\n"
            f"Response: {response.text}\n"
        )

        try:
            json_response = response.json()
        except JSONDecodeError:
            return response.text

        return self._handle_response(response, json_response)

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: dict = None,
        payload: dict = None,
        data_type=None,
        user_auth=True,
        headers=None,
    ):
        response = await self._request(
            method, endpoint, params, payload, user_auth, headers
        )
        if data_type:
            return self._construct_response(response, data_type)
        return response

    @staticmethod
    def _construct_response(data, data_type):
        if data_type is not None:
            if isinstance(data, list):
                data = [data_type(result) for result in data]
            elif data is not None:
                data = data_type(data)
        return data

    def _check_authorization(self) -> None:
        if self.session.headers.get("Authorization") is None:
            message = "Authorization is not present in the header."
            raise AuthenticationError(message)

    def _handle_response(self, response, json_response):
        translated_response = self._translate_error_message(json_response)
        if response.status_code == 400:
            raise BadRequestError(translated_response)
        if response.status_code == 401:
            raise AuthenticationError(translated_response)
        if response.status_code == 403:
            raise ForbiddenError(translated_response)
        if response.status_code == 404:
            raise NotFoundError(translated_response)
        if response.status_code == 429:
            raise RateLimitError(translated_response)
        if response.status_code == 500:
            raise YayServerError(translated_response)
        if response.status_code and not 200 <= response.status_code < 300:
            raise HTTPError(translated_response)
        return json_response

    def _translate_error_message(self, response):
        if self.err_lang == "ja":
            try:
                error_code = response.get("error_code", None)
                if error_code is not None:
                    error_type = ErrorType(error_code)
                    if error_type.name in ErrorMessage.__members__:
                        error_message = ErrorMessage[error_type.name].value
                        response["message"] = error_message
                return response
            except ValueError:
                return response
        else:
            return response

    def _generate_all_uuids(self):
        self.device_uuid = generate_uuid()[0]
        self.uuid, self.url_uuid = generate_uuid()


class AsyncClient(AsyncBaseClient):
    """

    API Client for asynchronous requests.

    """

    async def get_timeline(self, **params) -> PostsResponse:
        """

        タイムラインを取得します

        Parameters
        ----------

            - noreply_mode: bool - (optional)
            - from_post_id: int - (optional)
            - number: int - (optional)
            - order_by: str - (optional)
            - experiment_older_age_rules: bool - (optional)
            - shared_interest_categories: bool - (optional)
            - mxn: int - (optional)
            - en: int - (optional)
            - vn: int - (optional)
            - reduce_selfie: bool - (optional)
            - custom_generation_range: bool - (optional)

        """
        return await get_timeline(self, **params)

    async def get_user(self, user_id: int) -> User:
        """

        ユーザーの情報を取得します

        """
        return await get_user(self, user_id)
