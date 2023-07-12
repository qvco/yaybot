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

from ..config import Configs
from ..responses import ActivitiesResponse


def get_user_activities(self, **params) -> ActivitiesResponse:
    """

    Parameters
    ----------
        - important: bool - (required)
        - from_timestamp: int - (optional)
        - number: int - (optional)

    """
    self._check_authorization()
    return self._make_request(
        "GET",
        endpoint=f"https://{Configs.YAY_STAGING_HOST_2}/api/user_activities",
        params=params,
        data_type=ActivitiesResponse,
    )


def get_user_merged_activities(self, **params) -> ActivitiesResponse:
    """
    Parameters
    ----------

        - from_timestamp: int - (optional)
        - number: int - (optional)

    """
    self._check_authorization()
    return self._make_request(
        "GET",
        endpoint=f"https://{Configs.YAY_STAGING_HOST_2}/api/v2/user_activities",
        params=params,
        data_type=ActivitiesResponse,
    )


def received_notification(self, pid: str, type: str, opened_at: int = None):
    # TODO: opened_atはnullalbeか確認する
    self._check_authorization()
    return self._make_request(
        "POST",
        endpoint=f"{self.host}/api/received_push_notifications",
        payload={"pid": pid, "type": type, "opened_at": opened_at},
    )
