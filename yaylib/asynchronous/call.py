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

from typing import List

from ..config import Endpoints
from ..models import Bgm, ConferenceCall, Post
from ..responses import (
    BgmsResponse,
    CallStatusResponse,
    ConferenceCallResponse,
    GamesResponse,
    GenresResponse,
    PostResponse,
    PostsResponse,
    UsersByTimestampResponse,
)


def bump_call(self, call_id: int, participant_limit: int = None):
    params = {}
    if participant_limit:
        params["participant_limit"] = participant_limit
    response = self._make_request(
        "POST", endpoint=f"{Endpoints.CALLS_V1}/{call_id}/bump", params=params
    )
    self.logger.info("Call bumped.")
    return response


def get_user_active_call(self, user_id: int) -> Post:
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.POSTS_V1}/active_call",
        params={"user_id": user_id},
        data_type=PostResponse,
    ).post


def get_bgms(self) -> List[Bgm]:
    return self._make_request(
        "GET", endpoint=f"{Endpoints.CALLS_V1}/bgm", data_type=BgmsResponse
    ).bgm


def get_call(self, call_id: int) -> ConferenceCall:
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.CALLS_V1}/conferences/{call_id}",
        data_type=ConferenceCallResponse,
    ).conference_call


def get_call_invitable_users(
    self, call_id: int, from_timestamp: int = None
) -> UsersByTimestampResponse:
    # @Nullable @Query("user[nickname]")
    params = {}
    if from_timestamp:
        params["from_timestamp"] = from_timestamp
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.CALLS_V1}/{call_id}/users/invitable",
        params=params,
        data_type=UsersByTimestampResponse,
    )


def get_call_status(self, opponent_id: int) -> CallStatusResponse:
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.CALLS_V1}/phone_status/{opponent_id}",
        data_type=CallStatusResponse,
    )


def get_games(self, **params) -> GamesResponse:
    """

    Parameters
    ----------
        - number: int - (optional)
        - ids: List[int] - (optional)
        - from_id: int - (optional)

    """
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.GAMES_V1}/apps",
        params=params,
        data_type=GamesResponse,
    )


def get_genres(self, **params) -> GenresResponse:
    """

    Parameters
    ----------
        - number: int - (optional)
        - from: int - (optional)

    """
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.GENRES_V1}",
        params=params,
        data_type=GenresResponse,
    )


def get_group_calls(self, **params) -> PostsResponse:
    """

    Parameters
    ----------
        - number: int - (optional)
        - group_category_id: int - (optional)
        - from_timestamp: int - (optional)
        - scope: str - (optional)

    """
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.POSTS_V1}/group_calls",
        params=params,
        data_type=PostsResponse,
    )


def invite_to_call_bulk(self, call_id: int, group_id: int = None):
    """

    Parameters
    ----------
        - call_id: int - (required)
        - group_id: int - (optional)

    """
    params = {}
    if group_id:
        params["group_id"] = group_id
    response = self._make_request(
        "POST", endpoint=f"{Endpoints.CALLS_V1}/{call_id}/bulk_invite", params=params
    )
    self.logger.info("Invited your online followings to the call.")
    return response


def invite_users_to_call(self, call_id: int, user_ids: List[int]):
    """

    Parameters
    ----------
        - call_id: int - (required)
        - user_ids: List[int] - (required)

    """
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.CALLS_V1}/conference_calls/{call_id}/invite",
        payload={"call_id": call_id, "user_ids[]": user_ids},
    )
    self.logger.info("Invited users to call.")
    return response


def invite_users_to_chat_call(self, chat_room_id: int, room_id: int, room_url: str):
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.CALLS_V2}/invite",
        payload={
            "chat_room_id": chat_room_id,
            "room_id": room_id,
            "room_url": room_url,
        },
    )
    self.logger.info("Invited users to chat call.")
    return response


def kick_and_ban_from_call(self, call_id: int, user_id: int):
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.CALLS_V1}/conference_calls/{call_id}/kick",
        payload={"user_id": user_id},
    )
    self.logger.info("User has been banned from the call.")
    return response


def set_call(
    self,
    call_id: int,
    joinable_by: str,
    game_title: str = None,
    category_id: str = None,
):
    response = self._make_request(
        "PUT",
        endpoint=f"{Endpoints.CALLS_V1}/{call_id}",
        payload={
            "joinable_by": joinable_by,
            "game_title": game_title,
            "category_id": category_id,
        },
    )
    self.logger.info("Started a call")
    return response


def set_user_role(self, call_id: int, user_id: int, role: str):
    response = self._make_request(
        "PUT",
        endpoint=f"{Endpoints.CALLS_V1}/{call_id}/users/{user_id}",
        payload={"role": role},
    )
    self.logger.info(f"User '{user_id}' has been given a role.")
    return response


def start_call(self, conference_id: int, call_sid: str = None) -> ConferenceCall:
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.CALLS_V1}/start_conference_call",
        payload={"conference_id": conference_id, "call_sid": call_sid},
        data_type=ConferenceCallResponse,
    ).conference_call
    self.logger.info("Joined the call.")
    return response


def stop_call(self, conference_id: int, call_sid: str = None):
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.CALLS_V1}/leave_conference_call",
        payload={"conference_id": conference_id, "call_sid": call_sid},
    )
    self.logger.info("Left the call.")
    return response
