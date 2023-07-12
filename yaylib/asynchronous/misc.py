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
import httpx

from PIL import Image
from datetime import datetime
from typing import List

from ..config import Endpoints
from ..models import PresignedUrl
from ..responses import (
    EmailGrantTokenResponse,
    EmailVerificationPresignedUrlResponse,
    PresignedUrlResponse,
    PresignedUrlsResponse,
    IdCheckerPresignedUrlResponse,
    VerifyDeviceResponse,
    WebSocketTokenResponse,
)


def accept_policy_agreement(self, type: str):
    response = self._make_request(
        "POST", endpoint=f"{Endpoints.USERS_V1}/policy_agreements/{type}"
    )
    self.logger.info("Accepted to policy agreement.")
    return response


def generate_sns_thumbnail(self, **params):
    """

    Parameters:
    ----------

        - resource_type: str - (Required)
        - resource_id: int - (Required)

    """
    response = self._make_request(
        "GET", endpoint=f"{Endpoints.SNS_THUMBNAIL_V1}/generate", params=params
    )
    self.logger.info("SNS thumbnail generated.")
    return response


def send_verification_code(self, email: str):
    response = self._make_request(
        "POST",
        endpoint=self.get_email_verification_presigned_url(email=email, locale="ja"),
        payload={"locale": "ja", "email": email},
    )
    self.logger.info(f"Verification code successfully sent to '{email}'.")
    return response


def get_email_grant_token(self, code: int, email: str) -> EmailGrantTokenResponse:
    return self._make_request(
        "POST",
        endpoint=f"{Endpoints.GET_EMAIL_GRANT_TOKEN}",
        payload={"code": code, "email": email},
        data_type=EmailGrantTokenResponse,
    ).email_grant_token


def get_email_verification_presigned_url(
    self, email: str, locale: str, intent: str = None
) -> str:
    return self._make_request(
        "POST",
        endpoint=f"{Endpoints.EMAIL_VERIFICATION_URL_V1}",
        payload={
            "device_uuid": self.device_uuid,
            "email": email,
            "locale": locale,
            "intent": intent,
        },
        data_type=EmailVerificationPresignedUrlResponse,
    ).url


def get_file_upload_presigned_urls(self, file_names: List[str]) -> List[PresignedUrl]:
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.BUCKETS_V1}/presigned_urls",
        params={"file_names[]": file_names},
        data_type=PresignedUrlsResponse,
    ).presigned_urls


def get_id_checker_presigned_url(self, model: str, action: str, **params) -> str:
    # TODO: @QueryMap @NotNull Map<String, String> map
    """
    Meow..
    """
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.ID_CHECK_V1}/{model}/{action}",
        params=params,
        data_type=IdCheckerPresignedUrlResponse,
    ).presigned_url


def get_old_file_upload_presigned_url(self, video_file_name: str) -> str:
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.USERS_V1}/presigned_url",
        params={"video_file_name": video_file_name},
        data_type=PresignedUrlResponse,
    ).presigned_url


def get_web_socket_token(self, headers: dict = None) -> str:
    self._check_authorization()
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.USERS_V1}/ws_token",
        data_type=WebSocketTokenResponse,
        headers=headers,
    ).token


def verify_device(
    self, app_version: str, device_uuid: str, platform: str, verification_string: str
) -> VerifyDeviceResponse:
    # TODO: check platform, verification_string
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.GENUINE_DEVICES_V1}/verify",
        payload={
            "app_version": app_version,
            "device_uuid": device_uuid,
            "platform": platform,
            "verification_string": verification_string,
        },
        data_type=VerifyDeviceResponse,
    )
    self.logger.info("Device has been verified.")
    return response


def upload_image(self, image_type: str, image_path: str) -> str:
    """

    画像をアップロードしてattachment_filenameを返します。

    Parameteres
    -----------
        - image_type: str - (required): "post", "user_avatar" のどちらか
        - image_path: str - (required): "画像のパス

    """
    valid_types = ["post", "user_avatar"]
    if image_type not in valid_types:
        message = f"Invalid post type. Must be one of {valid_types}"
        raise ValueError(message)

    date = datetime.now()
    timestamp = int(date.timestamp() * 1000)
    filename, ext = os.path.splitext(image_path)

    with Image.open(image_path) as image:
        width, height = image.size

    base_url = f"{image_type}/{date.year}/{date.month}/{date.day}"
    mid_url = f"{filename}_{timestamp}_0_size_"
    original_url = f"{base_url}/{mid_url}{width}x{height}{ext}"
    thumb_url = f"{base_url}/thumb_{mid_url}{width}x{height}{ext}"

    presigned_urls = get_file_upload_presigned_urls(self, [original_url, thumb_url])

    with open(image_path, "rb") as f:
        response = httpx.put(presigned_urls[0].url, data=f.read())
        self._handle_response(response)

    with open(image_path, "rb") as f:
        response = httpx.put(presigned_urls[1].url, data=f.read())
        self._handle_response(response)

    self.logger.info(f"Image '{filename}{ext}' is uploaded")

    return presigned_urls[0].filename


def upload_video(self, video_path: str):
    pass
