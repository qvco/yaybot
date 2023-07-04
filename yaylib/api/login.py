from datetime import datetime
from typing import Dict, List

import os
import json

from ..config import *
from ..errors import *
from ..models import *
from ..responses import *
from ..utils import *


def change_email(
        self,
        email: str,
        password: str,
        email_grant_token: str = None
) -> LoginUpdateResponse:
    response = self._make_request(
        "PUT", endpoint=f"{Endpoints.USERS_V1}/change_email",
        payload={
            "api_key": self.api_key,
            "email": email,
            "password": password,
            "email_grant_token": email_grant_token
        }, data_type=LoginUpdateResponse
    )
    self.logger.info(self, fname="Your email has been changed.")
    return response


def change_password(
        self,
        current_password: str,
        new_password: str
) -> LoginUpdateResponse:
    response = self._make_request(
        "PUT", endpoint=f"{Endpoints.USERS_V1}/change_email",
        payload={
            "api_key": self.api_key,
            "current_password": current_password,
            "password": new_password
        }, data_type=LoginUpdateResponse
    )
    self.logger.info(self, fname="Your password has been changed..")
    return response


def connect_account_with_sns(self):
    pass


def disconnect_account_with_sns(self):
    pass


def get_token(
        self,
        grant_type: str,
        refresh_token: str = None,
        email: str = None,
        password: str = None
) -> TokenResponse:
    return self._make_request(
        "POST", endpoint=f"{self.host}/api/v1/oauth/token",
        payload={
            "grant_type": grant_type,
            "email": email,
            "password": password,
            "refresh_token": refresh_token
        }, data_type=TokenResponse
    )


def save_credentials(self, access_token, refresh_token, user_id, email=None):
    credentials = load_credentials(self)
    updated_credentials = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user_id": user_id,
        "email": email
    }
    if email is None:
        updated_credentials["email"] = credentials.get("email")
    with open(self.base_path + "credentials.json", "w") as f:
        json.dump(updated_credentials, f)


def load_credentials(self, check_email: str = None):
    """

    ローカルの認証情報が欠けているか存在しない場合はNoneを返す

    check_emailとローカルのメールアドレスが違う場合はNoneを返す

    """
    if not os.path.exists(self.base_path + "credentials.json"):
        return None

    with open(self.base_path + "credentials.json", "r") as f:
        credentials = json.load(f)

    result = all(key in credentials for key in (
        "access_token", "refresh_token", "user_id", "email"
    ))
    credentials = None if result is False else credentials

    if check_email is not None:
        credentials = None if check_email != credentials["email"] else credentials

    return credentials


def is_valid_token(self, access_token: str):
    headers = self.session.headers
    headers.setdefault("Authorization", f"Bearer {access_token}")
    try:
        self.get_web_socket_token(headers)
        return True
    except AuthenticationError:
        return False


def login(self, email: str, password: str) -> LoginUserResponse:

    # 既にローカルに保存されているか確認する
    credentials = load_credentials(self, email)
    # ローカルに保存されている場合
    if credentials is not None:
        self.session.headers.setdefault(
            "Authorization", f"Bearer {credentials['access_token']}"
        )
        self.logger.info(
            f"Successfully logged in as '{credentials['user_id']}'"
        )
        return credentials

    response = self._make_request(
        "POST", endpoint=f"{Endpoints.USERS_V3}/login_with_email",
        payload={
            "api_key": self.api_key,
            "email": email,
            "password": password,
            "uuid": self.uuid
        }, data_type=LoginUserResponse
    )
    message = "Invalid email or password."
    if response.access_token is None:
        raise ForbiddenError(message)

    self.session.headers.setdefault(
        "Authorization", f"Bearer {response.access_token}"
    )
    self.logger.info(
        f"Successfully logged in as '{response.user_id}'"
    )
    save_credentials(
        self,
        access_token=response.access_token,
        refresh_token=response.refresh_token,
        user_id=response.user_id,
        email=email
    )
    return response


def login_with_sns(self):
    pass


def logout(self):
    try:
        self._check_authorization()
        response = self._make_request(
            "POST", endpoint=f"{Endpoints.USERS_V1}/logout",
            payload={"uuid": self.uuid}
        )
        self.session.headers.pop("Authorization", None)
        self.logger.info("User has logged out.")
        return response

    except:
        self.logger.error("User is not logged in.")
        return None


def migrate_token(self):
    pass


def register_device_token(self):
    pass


def resend_confirm_email(self):
    return self._make_request(
        "POST", endpoint=f"{Endpoints.USERS_V2}/resend_confirm_email"
    )


def restore_user(self, user_id: int) -> LoginUserResponse:
    timestamp = int(datetime.now().timestamp())
    response = self._make_request(
        "POST", endpoint=f"{Endpoints.USERS_V2}/restore",
        payload={
            "user_id": user_id,
            "api_key": self.api_key,
            "uuid": self.uuid,
            "timestamp": timestamp,
            "signed_info": signed_info_calculating(
                self.device_uuid, timestamp
            ),
        }
    )
    self.logger.info("User has been restored.")
    return response


def revoke_tokens(self):
    response = self._make_request(
        "DELETE", endpoint=f"{Endpoints.USERS_V1}/device_tokens"
    )
    self.logger.info("Token has been revoked.")
    return response


def save_account_with_email(
        self,
        email: str,
        password: str = None,
        current_password: str = None,
        email_grant_token: str = None
) -> LoginUpdateResponse:
    response = self._make_request(
        "POST", endpoint=f"{Endpoints.USERS_V3}/login_update",
        payload={
            "api_key": self.api_key,
            "email": email,
            "password": password,
            "current_password": current_password,
            "email_grant_token": email_grant_token
        }, data_type=LoginUpdateResponse
    )
    self.logger.info("Account has been save with email.")
    return response
