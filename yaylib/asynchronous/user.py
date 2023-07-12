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

from datetime import datetime
from typing import Union, List

from ..config import Endpoints
from ..models import Footprint, User, UserWrapper
from ..responses import (
    ActiveFollowingsResponse,
    BlockedUserIdsResponse,
    BlockedUsersResponse,
    CreatePostResponse,
    CreateUserResponse,
    FollowRecommendationsResponse,
    FollowRequestCountResponse,
    FollowUsersResponse,
    FootprintsResponse,
    HiddenResponse,
    RefreshCounterRequestsResponse,
    SocialShareUsersResponse,
    UserResponse,
    UsersResponse,
    RankingUsersResponse,
    UserEmailResponse,
    HimaUsersResponse,
    UsersByTimestampResponse,
    UserTimestampResponse,
)
from ..utils import signed_info_calculating, signed_version_calculating


def delete_footprint(self, user_id: int, footprint_id: int):
    self._check_authorization()
    response = self._make_request(
        "DELETE", endpoint=f"{Endpoints.USERS_V2}/{user_id}/footprints/{footprint_id}"
    )
    self.logger.info("Footprint has been deleted.")
    return response


def destroy_user(self):
    self._check_authorization()
    answer = input("Are you sure you want to delete your account? Y/N")
    if answer.lower() != "y":
        return
    timestamp = int(datetime.now().timestamp())
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.USERS_V2}/destroy",
        payload={
            "uuid": self.uuid,
            "api_key": self.api_key,
            "timestamp": timestamp,
            "signed_info": signed_info_calculating(self.device_uuid, timestamp),
        },
    )
    self.logger.info("User has been deleted.")
    return response


def follow_user(self, user_id: int):
    self._check_authorization()
    response = self._make_request(
        "POST", endpoint=f"{Endpoints.USERS_V2}/{user_id}/follow"
    )
    self.logger.info(f"Followed the user '{user_id}'.")
    return response


def follow_users(self, user_ids: List[int]):
    self._check_authorization()
    response = self._make_request(
        "POST", endpoint=f"{Endpoints.USERS_V2}/follow", params={"user_ids[]": user_ids}
    )
    self.logger.info("Followed multiple users.")
    return response


def get_active_followings(self, **params) -> ActiveFollowingsResponse:
    """

    Parameters:
    ----------

        - only_online: bool
        - from_loggedin_at: int = None

    """
    self._check_authorization()
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.USERS_V1}/active_followings",
        params=params,
        data_type=ActiveFollowingsResponse,
    )


def get_follow_recommendations(self, **params) -> FollowRecommendationsResponse:
    """

    Parameters:
    ----------

        - from_timestamp: int = None,
        - number: int = None,
        - sources: List[str] = None

    """
    self._check_authorization()
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.FRIENDS_V1}",
        params=params,
        data_type=FollowRecommendationsResponse,
    )


def get_follow_request(self, from_timestamp: int = None) -> UsersByTimestampResponse:
    params = {}
    if from_timestamp:
        params["from_timestamp"] = from_timestamp
    self._check_authorization()
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.USERS_V2}/follow_requests",
        params=params,
        data_type=UsersByTimestampResponse,
    )


def get_follow_request_count(self) -> int:
    self._check_authorization()
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.USERS_V2}/follow_requests_count",
        data_type=FollowRequestCountResponse,
    ).users_count


def get_following_users_born(self, birthdate: int = None) -> UsersResponse:
    params = {}
    if birthdate:
        params["birthdate"] = birthdate
    self._check_authorization()
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.USERS_V1}/following_born_today",
        params=params,
        data_type=UsersResponse,
    )


def get_footprints(self, **params) -> List[Footprint]:
    """

    Parameters:
    ----------

        - from_id: int = None
        - number: int = None
        - mode: str = None

    """
    self._check_authorization()
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.USERS_V2}/footprints",
        params=params,
        data_type=FootprintsResponse,
    ).footprints


def get_fresh_user(self, user_id: int) -> UserResponse:
    self._check_authorization()
    return self._make_request(
        "GET", endpoint=f"{Endpoints.USERS_V2}/fresh/{user_id}", data_type=UserResponse
    )


def get_hima_users(self, **params) -> List[UserWrapper]:
    """

    Parameters:
    ----------

        - from_hima_id: int = None
        - number: int = None

    """
    self._check_authorization()
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.USERS_V2}/hima_users",
        params=params,
        data_type=HimaUsersResponse,
    ).hima_users


def get_user_ranking(self, mode: str) -> RankingUsersResponse:
    """

    ユーザーのランキングを取得します

    Examples:
    --------

    >>> ルーキーを取得する場合:

    >>> api.get_user_ranking(mode="one_month")

    ---

    >>> ミドルを取得する場合:

    >>> api.get_user_ranking(mode="six_months")

    ---

    >>> 殿堂入りを取得する場合:

    >>> api.get_user_ranking(mode="all_time")

    """
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.WEB_V1}/users/ranking",
        params={"mode": mode},
        data_type=RankingUsersResponse,
    )


def get_refresh_counter_requests(self) -> RefreshCounterRequestsResponse:
    self._check_authorization()
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.USERS_V1}/reset_counters",
        data_type=RefreshCounterRequestsResponse,
    )


def get_social_shared_users(self, **params) -> SocialShareUsersResponse:
    """

    Parameters:
    ----------

        - sns_name: str - (Required)
        - number: int - (Optional)
        - from_id: int - (Optional)

    """
    self._check_authorization()
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.USERS_V2}/social_shared_users",
        params=params,
        data_type=SocialShareUsersResponse,
    )


def get_timestamp(self) -> UserTimestampResponse:
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.USERS_V2}/timestamp",
        data_type=UserTimestampResponse,
    )


def get_user(self, user_id: int) -> User:
    return self._make_request(
        "GET", endpoint=f"{Endpoints.USERS_V2}/{user_id}", data_type=UserResponse
    ).user


def get_user_email(self, user_id: int) -> str:
    self._check_authorization()
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.USERS_V2}/fresh/{user_id}",
        data_type=UserEmailResponse,
    ).email


def get_user_followers(self, user_id: int, **params) -> FollowUsersResponse:
    """

    Parameters:
    ----------

        - user_id: int - (required)
        - from_follow_id: int - (optional)
        - followed_by_me: int - (optional)
        - number: int - (optional)

    """
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.USERS_V2}/{user_id}/followers",
        params=params,
        data_type=FollowUsersResponse,
    )


def get_user_followings(self, user_id: int, **params) -> FollowUsersResponse:
    # @Body @Nullable SearchUsersRequest searchUsersRequest
    """

    Parameters:
    ----------

        - user_id: int
        - from_follow_id: int = None
        - from_timestamp: int = None
        - order_by: str = None
        - number: int - (optional)

    """
    self._check_authorization()
    return self._make_request(
        "POST",
        endpoint=f"{Endpoints.USERS_V2}/{user_id}/list_followings",
        params=params,
        data_type=FollowUsersResponse,
    )


def get_user_from_qr(self, qr: str) -> UserResponse:
    return self._make_request(
        "GET", endpoint=f"{Endpoints.USERS_V1}/qr_codes/{qr}", data_type=UserResponse
    )


def get_user_without_leaving_footprint(self, user_id: int) -> UserResponse:
    return self._make_request(
        "GET", endpoint=f"{Endpoints.USERS_V2}/info/{user_id}", data_type=UserResponse
    )


def get_users(self, user_ids: List[int]) -> UsersResponse:
    headers = self.session.headers
    headers["X-Jwt"] = self.get_web_socket_token()
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.USERS_V1}/list_id",
        params={"user_ids[]": user_ids},
        data_type=UsersResponse,
        headers=headers,
    )


def reduce_kenta_penalty(self, user_id: int):
    self._check_authorization()
    timestamp = int(datetime.now().timestamp())
    response = self._make_request(
        "POST",
        endpoint=f"{self.host}api/v3/users/{user_id}/reduce_penalty",
        payload={
            "uuid": self.uuid,
            "api_key": self.api_key,
            "timestamp": timestamp,
            "signed_info": signed_info_calculating(self.device_uuid, timestamp),
            "signed_version": signed_version_calculating(),
        },
        data_type=CreatePostResponse,
    )
    self.logger.info("Penalty has been reduced.")
    return response


def refresh_counter(self, counter: str):
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.USERS_V1}/reset_counters",
        payload={"counter": counter},
    )
    self.logger.info("Requested counter refresh.")
    return response


def register_user(
    self,
    email: str,
    email_grant_token: str,
    password: str,
    nickname: str,
    birth_date: str,
    gender: int = -1,
    country_code: str = "JP",
    biography: str = None,
    prefecture: str = None,
    profile_icon_filename: str = None,
    cover_image_filename: str = None,
    # @Nullable @Part("sns_info") SignUpSnsInfoRequest signUpSnsInfoRequest,
    en: int = None,
    vn: int = None,
) -> CreateUserResponse:
    timestamp = int(datetime.now().timestamp())
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.USERS_V3}/register",
        payload={
            "app_version": self.api_version,
            "timestamp": timestamp,
            "api_key": self.api_key,
            "signed_version": signed_version_calculating(),
            "signed_info": signed_info_calculating(self.device_uuid, timestamp),
            "uuid": self.uuid,
            "nickname": nickname,
            "birth_date": birth_date,
            "gender": gender,
            "country_code": country_code,
            "biography": biography,
            "prefecture": prefecture,
            "profile_icon_filename": profile_icon_filename,
            "cover_image_filename": cover_image_filename,
            "email": email,
            "password": password,
            "email_grant_token": email_grant_token,
            "en": en,
            "vn": vn,
        },
        data_type=CreateUserResponse,
    )
    self.logger.info(f"A new user has been registered. (USER ID: {response.id})")
    return response


def remove_user_avatar(self):
    response = self._make_request(
        "POST", endpoint=f"{Endpoints.USERS_V2}/remove_profile_photo"
    )
    self.logger.info("Profile image has been removed.")
    return response


def remove_user_cover(self):
    response = self._make_request(
        "POST", endpoint=f"{Endpoints.USERS_V2}/remove_cover_image"
    )
    self.logger.info("Profile cover image has been removed.")
    return response


def report_user(
    self,
    user_id: int,
    category_id: int,
    reason: str = None,
    screenshot_filename: str = None,
    screenshot_2_filename: str = None,
    screenshot_3_filename: str = None,
    screenshot_4_filename: str = None,
):
    self._check_authorization()
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.USERS_V3}/{user_id}/report",
        payload={
            "category_id": category_id,
            "reason": reason,
            "screenshot_filename": screenshot_filename,
            "screenshot_2_filename": screenshot_2_filename,
            "screenshot_3_filename": screenshot_3_filename,
            "screenshot_4_filename": screenshot_4_filename,
        },
    )
    self.logger.info(f"Reported the user '{user_id}'")
    return response


def reset_password(self, email: str, email_grant_token: str, password: str):
    response = self._make_request(
        "PUT",
        endpoint=f"{Endpoints.USERS_V1}/reset_password",
        payload={
            "email": email,
            "email_grant_token": email_grant_token,
            "password": password,
        },
    )
    self.logger.info("Reset the password.")
    return response


def search_lobi_users(self, **params) -> UsersResponse:
    """

    Parameters:
    ----------

        - nickname: str = None
        - number: int = None
        - from_str: str = None

    """
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.LOBI_FRIENDS_V1}",
        params=params,
        data_type=UsersResponse,
    )


def search_users(self, **params) -> UsersResponse:
    """

    Parameters:
    ----------

        - gender: int = None
        - nickname: str = None
        - title: str = None
        - biography: str = None
        - from_timestamp: int = None
        - similar_age: bool = None
        - not_recent_gomimushi: bool = None
        - recently_created: bool = None
        - same_prefecture: bool = None
        - save_recent_search: bool = None

    """
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.USERS_V1}/search",
        params=params,
        data_type=UsersResponse,
    )


def set_follow_permission_enabled(self, nickname: str, is_private: bool = None):
    timestamp = int(datetime.now().timestamp())
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.USERS_V2}/edit",
        payload={
            "nickname": nickname,
            "is_private": is_private,
            "uuid": self.uuid,
            "api_key": self.api_key,
            "timestamp": timestamp,
            "signed_info": signed_info_calculating(self.device_uuid, timestamp),
            "signed_version": signed_version_calculating(),
        },
    )
    self.logger.info("Follow permission has been enabled.")
    return response


def set_setting_follow_recommendation_enabled(self, on: bool):
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.USERS_V1}/visible_on_sns_friend_recommendation_setting",
        params={"on": on},
    )
    self.logger.info("Follow recommendation has been enabled.")
    return response


def take_action_follow_request(self, target_id: int, action: str):
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.USERS_V2}/{target_id}/follow_request",
        payload={"action": action},
    )
    self.logger.info("Took action follow request.")
    return response


def turn_on_hima(self):
    self._check_authorization()
    response = self._make_request(
        "GET",
        endpoint=f"{Endpoints.USERS_V1}/hima",
    )
    self.logger.info("Turned on 'hima now'.")
    return response


def unfollow_user(self, user_id: int):
    self._check_authorization()
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.USERS_V2}/{user_id}/unfollow",
    )
    self.logger.info(f"Unfollowed the user '{user_id}'")
    return response


def update_language(self, language: str):
    timestamp = int(datetime.now().timestamp())
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.USERS_V1}/language",
        payload={
            "uuid": self.uuid,
            "api_key": self.api_key,
            "timestamp": timestamp,
            "signed_info": signed_info_calculating(self.device_uuid, timestamp),
            "language": language,
        },
    )
    self.logger.info("Language has been updated.")
    return response


def update_user(
    self,
    nickname: str,
    biography: str = None,
    prefecture: str = None,
    gender: int = None,
    country_code: str = None,
    profile_icon_filename: str = None,
    cover_image_filename: str = None,
    username: str = None,
):
    self._check_authorization()
    timestamp = int(datetime.now().timestamp())
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.USERS_V3}/edit",
        payload={
            "nickname": nickname,
            "biography": biography,
            "prefecture": prefecture,
            "gender": gender,
            "country_code": country_code,
            "profile_icon_filename": profile_icon_filename,
            "cover_image_filename": cover_image_filename,
            "username": username,
            "uuid": self.uuid,
            "api_key": self.api_key,
            "timestamp": timestamp,
            "signed_info": signed_info_calculating(self.device_uuid, timestamp),
        },
    )
    self.logger.info("User profile has been updated.")
    return response


# BlockApi


def block_user(self, user_id: int):
    self._check_authorization()
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.USERS_V1}/{user_id}/block",
    )
    self.logger.info(f"Blocked the user '{user_id}'")
    return response


def get_blocked_user_ids(self) -> BlockedUserIdsResponse:
    self._check_authorization()
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.USERS_V1}/block_ids",
        data_type=BlockedUserIdsResponse,
    )


def get_blocked_users(self, from_id: int = None) -> BlockedUsersResponse:
    # @Body @NotNull SearchUsersRequest searchUsersRequest
    self._check_authorization()
    params = {}
    if from_id:
        params["from_id"] = from_id
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.USERS_V2}/blocked",
        params=params,
        data_type=BlockedUsersResponse,
    )


def unblock_user(self, user_id: int):
    self._check_authorization()
    response = self._make_request(
        "POST", endpoint=f"{Endpoints.USERS_V2}/{user_id}/unblock"
    )
    self.logger.info(f"Unblocked the user '{user_id}'")
    return response


# HiddenApi


def get_hidden_users_list(self, **params: Union[str, int]) -> HiddenResponse:
    """

    Parameters:
    ----------

        - from: str = None
        - number: int = None

    """
    self._check_authorization()
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.HIDDEN_V1}/users",
        params=params,
        data_type=HiddenResponse,
    )


def hide_user(self, user_id: int):
    self._check_authorization()
    response = self._make_request(
        "POST", endpoint=f"{Endpoints.HIDDEN_V1}/users", payload={"user_id": user_id}
    )
    self.logger.info(f"User '{user_id}' is hidden")
    return response


def unhide_users(self, user_ids: List[int]):
    self._check_authorization()
    response = self._make_request(
        "DELETE",
        endpoint=f"{Endpoints.HIDDEN_V1}/users",
        params={"user_ids[]": user_ids},
    )
    self.logger.info("Unhid users")
    return response
