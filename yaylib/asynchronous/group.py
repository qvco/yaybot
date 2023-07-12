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
from typing import List

from ..config import Endpoints
from ..models import CreateGroupQuota
from ..responses import (
    CreateGroupResponse,
    GroupCategoriesResponse,
    GroupResponse,
    GroupsRelatedResponse,
    GroupsResponse,
    GroupUserResponse,
    GroupUsersResponse,
    UnreadStatusResponse,
    UsersResponse,
    UsersByTimestampResponse,
)
from ..utils import signed_info_calculating


def accept_moderator_offer(self, group_id: int):
    self._check_authorization()
    response = self._make_request(
        "PUT", endpoint=f"{Endpoints.GROUPS_V1}/{group_id}/deputize"
    )
    self.logger.info("Accepted the group moderator offer.")
    return response


def accept_ownership_offer(self, group_id: int):
    self._check_authorization()
    response = self._make_request(
        "PUT", endpoint=f"{Endpoints.GROUPS_V1}/{group_id}/transfer"
    )
    self.logger.info("Accepted the group ownership offer.")
    return response


def accept_group_join_request(self, group_id: int, user_id: int):
    self._check_authorization()
    response = self._make_request(
        "POST", endpoint=f"{Endpoints.GROUPS_V1}/{group_id}/accept/{user_id}"
    )
    self.logger.info("Accepted the group join request.")
    return response


def add_related_groups(self, group_id: int, related_group_id: List[int]):
    """

    関連サークルを追加する

    """
    self._check_authorization()
    response = self._make_request(
        "PUT",
        endpoint=f"{Endpoints.GROUPS_V1}/{group_id}/related",
        params={"related_group_id[]": related_group_id},
    )
    self.logger.info("Group has been added to the related groups")
    return response


def ban_group_user(self, group_id: int, user_id: int):
    self._check_authorization()
    response = self._make_request(
        "POST", endpoint=f"{Endpoints.GROUPS_V1}/{group_id}/ban/{user_id}"
    )
    self.logger.info(f"User '{user_id}' has been banned from the group.")
    return response


def check_unread_status(self, from_time: int = None) -> UnreadStatusResponse:
    self._check_authorization()
    params = {}
    if from_time:
        params["from_time"] = from_time
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.GROUPS_V1}/unread_status",
        params=params,
        data_type=UnreadStatusResponse,
    )


def create_group(
    self,
    topic: str,
    description: str = None,
    secret: bool = None,
    hide_reported_posts: bool = None,
    hide_conference_call: bool = None,
    is_private: bool = None,
    only_verified_age: bool = None,
    only_mobile_verified: bool = None,
    call_timeline_display: bool = None,
    allow_ownership_transfer: bool = None,
    allow_thread_creation_by: str = None,
    gender: int = None,
    generation_groups_limit: int = None,
    group_category_id: int = None,
    cover_image_filename: str = None,
    sub_category_id: str = None,
    hide_from_game_eight: bool = None,
    allow_members_to_post_media: bool = None,
    allow_members_to_post_url: bool = None,
    guidelines: str = None,
) -> CreateGroupResponse:
    self._check_authorization()
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.GROUPS_V3}/new",
        payload={
            "topic": topic,
            "description": description,
            "secret": secret,
            "hide_reported_posts": hide_reported_posts,
            "hide_conference_call": hide_conference_call,
            "is_private": is_private,
            "only_verified_age": only_verified_age,
            "only_mobile_verified": only_mobile_verified,
            "call_timeline_display": call_timeline_display,
            "allow_ownership_transfer": allow_ownership_transfer,
            "allow_thread_creation_by": allow_thread_creation_by,
            "gender": gender,
            "generation_groups_limit": generation_groups_limit,
            "group_category_id": group_category_id,
            "cover_image_filename": cover_image_filename,
            "uuid": self.uuid,
            "api_key": self.api_key,
            "timestamp": int(datetime.now().timestamp()),
            "signed_info": signed_info_calculating(
                self.api_key, self.device_uuid, int(datetime.now().timestamp())
            ),
            "sub_category_id": sub_category_id,
            "hide_from_game_eight": hide_from_game_eight,
            "allow_members_to_post_image_and_video": allow_members_to_post_media,
            "allow_members_to_post_url": allow_members_to_post_url,
            "guidelines": guidelines,
        },
        data_type=CreateGroupResponse,
    )
    self.logger.info("Group has been created.")
    return response


def create_pin_group(self, group_id: int):
    self._check_authorization()
    response = self._make_request(
        "POST", endpoint=f"{Endpoints.PINNED_V1}/groups", payload={"id": group_id}
    )
    self.logger.info("Pinned the group.")
    return response


def decline_moderator_offer(self, group_id: int):
    self._check_authorization()
    response = self._make_request(
        "DELETE", endpoint=f"{Endpoints.GROUPS_V1}/{group_id}/deputize"
    )
    self.logger.info("Declined the moderator offer.")
    return response


def decline_ownership_offer(self, group_id: int):
    self._check_authorization()
    response = self._make_request(
        "DELETE", endpoint=f"{Endpoints.GROUPS_V1}/{group_id}/transfer"
    )
    self.logger.info("Declined the ownership offer.")
    return response


def decline_group_join_request(self, group_id: int, user_id: int):
    self._check_authorization()
    response = self._make_request(
        "POST", endpoint=f"{Endpoints.GROUPS_V1}/{group_id}/decline/{user_id}"
    )
    self.logger.info("Declined the group join request.")
    return response


def delete_pin_group(self, group_id: int):
    self._check_authorization()
    response = self._make_request(
        "DELETE", endpoint=f"{Endpoints.PINNED_V1}/groups/{group_id}"
    )
    self.logger.info("Unpinned the group.")
    return response


def get_banned_group_members(self, group_id: int, page: int = None) -> UsersResponse:
    self._check_authorization()
    params = {}
    if page:
        params["page"] = page
    return self._make_request(
        "GET", endpoint=f"{Endpoints.GROUPS_V1}/{group_id}/ban_list", params=params
    )


def get_group_categories(self, **params) -> GroupCategoriesResponse:
    """

    Parameters:
    ----------

        - page: int - (optional)
        - number: int - (optional)

    """
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.GROUPS_V1}/categories",
        params=params,
        data_type=GroupCategoriesResponse,
    )


def get_create_group_quota(self) -> CreateGroupQuota:
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.GROUPS_V1}/created_quota",
        data_type=CreateGroupQuota,
    ).create


def get_group(self, group_id: int) -> GroupResponse:
    return self._make_request(
        "GET", endpoint=f"{Endpoints.GROUPS_V1}/{group_id}", data_type=GroupResponse
    )


def get_groups(self, **params) -> GroupsResponse:
    """

    Parameters:
    ----------

        - group_category_id: int = None
        - keyword: str = None
        - from_timestamp: int = None
        - sub_category_id: int = None

    """
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.GROUPS_V2}",
        params=params,
        data_type=GroupsResponse,
    )


def get_invitable_users(self, group_id: int, **params) -> UsersByTimestampResponse:
    """

    Parameters:
    ----------

        - from_timestamp: int - (optional)
        - user[nickname]: str - (optional)

    """
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.GROUPS_V1}/{group_id}/users/invitable",
        params=params,
        data_type=UsersByTimestampResponse,
    )


def get_joined_statuses(self, ids: List[int]) -> dict:
    self._check_authorization()
    return self._make_request(
        "GET", endpoint=f"{Endpoints.GROUPS_V1}/joined_statuses", params={"ids[]": ids}
    )


def get_group_member(self, group_id: int, user_id: int) -> GroupUserResponse:
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.GROUPS_V1}/{group_id}/members/{user_id}",
    )


def get_group_members(self, group_id: int, **params) -> GroupUsersResponse:
    """

    Parameters:
    ----------

        - id: int - (required)
        - mode: str - (optional)
        - keyword: str - (optional)
        - from_id: int - (optional)
        - from_timestamp: int - (optional)
        - order_by: str - (optional)
        - followed_by_me: bool - (optional)

    """
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.GROUPS_V2}/{group_id}/members",
        params=params,
        data_type=GroupUsersResponse,
    )


def get_my_groups(self, from_timestamp: None) -> GroupsResponse:
    self._check_authorization()
    params = {}
    if from_timestamp:
        params["from_timestamp"] = from_timestamp
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.GROUPS_V2}/mine",
        params=params,
        data_type=GroupsResponse,
    )


def get_relatable_groups(self, group_id: int, **params) -> GroupsRelatedResponse:
    """

    Parameters:
    ----------

        - group_id: int - (required)
        - keyword: str - (optional)
        - from: str - (optional)

    """
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.GROUPS_V1}/{group_id}/relatable",
        params=params,
        data_type=GroupsRelatedResponse,
    )


def get_related_groups(self, group_id: int, **params) -> GroupsRelatedResponse:
    """

    Parameters:
    ----------

        - group_id: int - (required)
        - keyword: str - (optional)
        - from: str - (optional)

    """
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.GROUPS_V1}/{group_id}/related",
        params=params,
        data_type=GroupsRelatedResponse,
    )


def get_user_groups(self, **params) -> GroupsResponse:
    """

    Parameters:
    ----------

        - user_id: int - (required)
        - page: int - (optional)

    """
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.GROUPS_V1}/user_group_list",
        params=params,
        data_type=GroupsResponse,
    )


def invite_users_to_group(self, group_id: int, user_ids: List[int]):
    self._check_authorization()
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.GROUPS_V1}/{group_id}/invite",
        payload={"user_ids[]": user_ids},
    )
    self.logger.info("Invited users to the group.")
    return response


def join_group(self, group_id: int):
    self._check_authorization()
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.GROUPS_V1}/{group_id}/join",
    )
    self.logger.info("You are now one of the members of the group.")
    return response


def leave_group(self, group_id: int):
    self._check_authorization()
    response = self._make_request(
        "DELETE",
        endpoint=f"{Endpoints.GROUPS_V1}/{group_id}/leave",
    )
    self.logger.info("Left the group.")
    return response


def post_gruop_social_shared(self, group_id: int, sns_name: str):
    self._check_authorization()
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.GROUPS_V2}/{group_id}/social_shared",
        params={"sns_name": sns_name},
    )
    self.logger.info("Group social shared has been posted.")
    return response


def remove_group_cover(self, group_id: int):
    self._check_authorization()
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.GROUPS_V1}/{group_id}/remove_cover",
    )
    self.logger.info("Group cover image has been removed.")
    return response


def remove_moderator(self, group_id: int, user_id: int):
    self._check_authorization()
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.GROUPS_V1}/{group_id}/fire/{user_id}",
    )
    self.logger.info(f"Group moderator '{user_id}' has been removed.")
    return response


def remove_related_groups(self, group_id: int, related_group_ids: List[int]):
    self._check_authorization()
    response = self._make_request(
        "DELETE",
        endpoint=f"{Endpoints.GROUPS_V1}/{group_id}/related",
        params={"related_group_id[]": related_group_ids},
    )
    self.logger.info("Related groups have been removed.")
    return response


def report_group(
    self,
    group_id: int,
    category_id: int,
    reason: str = None,
    opponent_id: int = None,
    screenshot_filename: str = None,
    screenshot_2_filename: str = None,
    screenshot_3_filename: str = None,
    screenshot_4_filename: str = None,
):
    self._check_authorization()
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.GROUPS_V3}/{group_id}/report",
        payload={
            "category_id": category_id,
            "reason": reason,
            "opponent_id": opponent_id,
            "screenshot_filename": screenshot_filename,
            "screenshot_2_filename": screenshot_2_filename,
            "screenshot_3_filename": screenshot_3_filename,
            "screenshot_4_filename": screenshot_4_filename,
        },
    )
    self.logger.info("Group has been reported.")
    return response


def send_moderator_offers(self, group_id: int, user_ids: List[int]):
    self._check_authorization()
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.GROUPS_V3}/{group_id}/deputize/mass",
        payload={
            "user_ids[]": user_ids,
            "uuid": self.uuid,
            "api_key": self.api_key,
            "timestamp": int(datetime.now().timestamp()),
            "signed_info": signed_info_calculating(
                self.api_key, self.device_uuid, int(datetime.now().timestamp())
            ),
        },
    )
    self.logger.info("Offered users to become a group moderator.")
    return response


def send_ownership_offer(self, group_id: int, user_id: int):
    self._check_authorization()
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.GROUPS_V3}/{group_id}/transfer",
        payload={
            "user_id": user_id,
            "uuid": self.uuid,
            "api_key": self.api_key,
            "timestamp": int(datetime.now().timestamp()),
            "signed_info": signed_info_calculating(
                self.api_key, self.device_uuid, int(datetime.now().timestamp())
            ),
        },
    )
    self.logger.info("Offered user to become a group owner.")
    return response


def set_group_title(self, group_id: int, title: str):
    self._check_authorization()
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.GROUPS_V1}/{group_id}/set_title",
        payload={"title": title},
    )
    self.logger.info("Group tittle has been set.")
    return response


def take_over_group_ownership(self, group_id: int):
    self._check_authorization()
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.GROUPS_V1}/{group_id}/take_over",
    )
    self.logger.info(f"Took over the group ownership of {group_id}")
    return response


def unban_group_member(self, group_id: int, user_id: int):
    self._check_authorization()
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.GROUPS_V1}/{group_id}/unban/{user_id}",
    )
    self.logger.info("User has been banned from the group.")
    return response


def update_group(
    self,
    group_id: int,
    topic: str,
    description: str = None,
    secret: bool = None,
    hide_reported_posts: bool = None,
    hide_conference_call: bool = None,
    is_private: bool = None,
    only_verified_age: bool = None,
    only_mobile_verified: bool = None,
    call_timeline_display: bool = None,
    allow_ownership_transfer: bool = None,
    allow_thread_creation_by: str = None,
    gender: int = None,
    generation_groups_limit: int = None,
    group_category_id: int = None,
    cover_image_filename: str = None,
    sub_category_id: str = None,
    hide_from_game_eight: bool = None,
    allow_members_to_post_media: bool = None,
    allow_members_to_post_url: bool = None,
    guidelines: str = None,
) -> GroupResponse:
    self._check_authorization()
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.GROUPS_V3}/{group_id}/update",
        payload={
            "topic": topic,
            "description": description,
            "secret": secret,
            "hide_reported_posts": hide_reported_posts,
            "hide_conference_call": hide_conference_call,
            "is_private": is_private,
            "only_verified_age": only_verified_age,
            "only_mobile_verified": only_mobile_verified,
            "call_timeline_display": call_timeline_display,
            "allow_ownership_transfer": allow_ownership_transfer,
            "allow_thread_creation_by": allow_thread_creation_by,
            "gender": gender,
            "generation_groups_limit": generation_groups_limit,
            "group_category_id": group_category_id,
            "cover_image_filename": cover_image_filename,
            "sub_category_id": sub_category_id,
            "uuid": self.uuid,
            "api_key": self.api_key,
            "timestamp": int(datetime.now().timestamp()),
            "signed_info": signed_info_calculating(
                self.api_key, self.device_uuid, int(datetime.now().timestamp())
            ),
            "hide_from_game_eight": hide_from_game_eight,
            "allow_members_to_post_image_and_video": allow_members_to_post_media,
            "allow_members_to_post_url": allow_members_to_post_url,
            "guidelines": guidelines,
        },
        data_type=GroupResponse,
    )
    self.logger.info("Group details have been updated.")
    return response


def withdraw_moderator_offer(self, group_id: int, user_id: int):
    self._check_authorization()
    response = self._make_request(
        "PUT",
        endpoint=f"{Endpoints.GROUPS_V1}/{group_id}/deputize/{user_id}/withdraw",
    )
    self.logger.info("Group moderator offer has been withdrawn")
    return response


def withdraw_ownership_offer(self, group_id: int, user_id: int):
    self._check_authorization()
    response = self._make_request(
        "PUT",
        endpoint=f"{Endpoints.GROUPS_V1}/{group_id}/transfer/withdraw",
        payload={"user_id": user_id},
    )
    self.logger.info("Group ownership offer has been withdrawn")
    return response
