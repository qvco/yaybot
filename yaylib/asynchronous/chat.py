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
from ..models import ChatRoom, GifImageCategory, Message, StickerPack
from ..responses import (
    ChatRoomResponse,
    ChatRoomsResponse,
    TotalChatRequestResponse,
    CreateChatRoomResponse,
    FollowUsersResponse,
    GifsDataResponse,
    MessageResponse,
    MessagesResponse,
    StickerPacksResponse,
    UnreadStatusResponse,
)


def accept_chat_request(self, chat_room_ids: List[int]):
    self._check_authorization()
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.CHAT_ROOMS_V1}/accept_chat_request",
        payload={"chat_room_ids[]": chat_room_ids},
    )
    self.logger.info("Accepted chat requests")
    return response


def check_unread_status(self, from_time: int) -> UnreadStatusResponse:
    self._check_authorization()
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.CHAT_ROOMS_V1}/unread_status",
        params={"from_time": from_time},
        data_type=UnreadStatusResponse,
    )


def create_group_chat(
    self,
    name: str,
    with_user_ids: List[int],
    icon_filename: str = None,
    background_filename: str = None,
) -> CreateChatRoomResponse:
    self._check_authorization()
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.CHAT_ROOMS_V3}/new",
        payload={
            "name": name,
            "with_user_ids[]": with_user_ids,
            "icon_filename": icon_filename,
            "background_filename": background_filename,
        },
        data_type=CreateChatRoomResponse,
    )
    self.logger.info(f"Group chat '{name}' has been created.")
    return response


def create_private_chat(
    self, with_user_id: int, matching_id: int = None, hima_chat: bool = False
) -> CreateChatRoomResponse:
    self._check_authorization()
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.CHAT_ROOMS_V1}/new",
        payload={
            "with_user_id": with_user_id,
            "matching_id": matching_id,
            "hima_chat": hima_chat,
        },
        data_type=CreateChatRoomResponse,
    )
    self.logger.info(f"Created a private chatroom with '{with_user_id}'.")
    return response


def delete_background(self, room_id: int):
    self._check_authorization()
    response = self._make_request(
        "DELETE",
        endpoint=f"{Endpoints.CHAT_ROOMS_V2}/{room_id}/background",
    )
    self.logger.info("Background image of the chatroom has been deleted.")
    return response


def delete_message(self, room_id: int, message_id: int):
    self._check_authorization()
    response = self._make_request(
        "DELETE",
        endpoint=f"{Endpoints.CHAT_ROOMS_V1}/{room_id}/messages/{message_id}/delete",
    )
    self.logger.info("Message has been deleted.")
    return response


def edit_chat_room(
    self,
    chat_room_id: int,
    name: str,
    icon_filename: str = None,
    background_filename: str = None,
):
    self._check_authorization()
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.CHAT_ROOMS_V1}/{chat_room_id}/edit",
        payload={
            "name": name,
            "icon_filename": icon_filename,
            "background_filename": background_filename,
        },
    )
    self.logger.info("Chatroom has been updated.")
    return response


def get_chatable_users(
    self,
    # @Body @Nullable SearchUsersRequest searchUsersRequest
    from_follow_id: int = None,
    from_timestamp: int = None,
    order_by: str = None,
) -> FollowUsersResponse:
    self._check_authorization()
    return self._make_request(
        "POST",
        endpoint=f"{Endpoints.USERS_V1}/followings/chatable",
        payload={
            "from_follow_id": from_follow_id,
            "from_timestamp": from_timestamp,
            "order_by": order_by,
        },
        data_type=FollowUsersResponse,
    )


def get_gifs_data(self) -> List[GifImageCategory]:
    self._check_authorization()
    return self._make_request(
        "GET", endpoint=f"{Endpoints.HIDDEN_V1}/chats", data_type=GifsDataResponse
    ).gif_categories


def get_hidden_chat_rooms(self, **params) -> ChatRoomsResponse:
    """

    Parameters:
    ---------------

        - from_timestamp: int - (optional)
        - number: int - (optional)

    """
    self._check_authorization()
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.HIDDEN_V1}/chats",
        params=params,
        data_type=ChatRoomsResponse,
    )


def get_main_chat_rooms(self, from_timestamp: int = None) -> ChatRoomsResponse:
    self._check_authorization()
    params = {}
    if from_timestamp:
        params["from_timestamp"] = from_timestamp
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.CHAT_ROOMS_V1}/main_list",
        params=params,
        data_type=ChatRoomsResponse,
    )


def get_messages(self, chat_room_id: int, **params) -> List[Message]:
    """

    Parameters:
    ---------------
        - from_message_id: int - (optional)
        - to_message_id: int - (optional)

    """
    self._check_authorization()
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.CHAT_ROOMS_V2}/{chat_room_id}/messages",
        params=params,
        data_type=MessagesResponse,
    ).messages


def get_request_chat_rooms(self, from_timestamp: int = None) -> ChatRoomsResponse:
    self._check_authorization()
    params = {}
    if from_timestamp:
        params["from_timestamp"] = from_timestamp
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.CHAT_ROOMS_V1}/request_list",
        params=params,
        data_type=ChatRoomsResponse,
    )


def get_chat_room(self, chat_room_id: int) -> ChatRoom:
    self._check_authorization()
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.CHAT_ROOMS_V2}/{chat_room_id}",
        data_type=ChatRoomResponse,
    ).chat


def get_sticker_packs(self) -> List[StickerPack]:
    return self._make_request(
        "GET", endpoint=Endpoints.STICKER_PACKS_V2, data_type=StickerPacksResponse
    ).sticker_packs


def get_total_chat_requests(self) -> int:
    self._check_authorization()
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.CHAT_ROOMS_V1}/total_chat_request",
        data_type=TotalChatRequestResponse,
    ).total


def hide_chat(self, chat_room_id: int):
    self._check_authorization()
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.HIDDEN_V1}/chats",
        payload={"chat_room_id": chat_room_id},
    )
    self.logger.info(f"Chatroom '{chat_room_id}' has been hidden.")
    return response


def invite_to_chat(self, chat_room_id: int, user_ids: List[int]):
    self._check_authorization()
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.CHAT_ROOMS_V2}/{chat_room_id}/invite",
        payload={"with_user_ids[]": user_ids},
    )
    self.logger.info("Invited users to the chatroom.")
    return response


def kick_users_from_chat(self, chat_room_id: int, user_ids: List[int]):
    self._check_authorization()
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.CHAT_ROOMS_V2}/{chat_room_id}/kick",
        payload={"with_user_ids[]": user_ids},
    )
    self.logger.info(f"Users have been kicked from the chatroom.")
    return response


def pin_chat(self, room_id: int):
    self._check_authorization()
    response = self._make_request(
        "POST", endpoint=f"{Endpoints.CHAT_ROOMS_V1}/{room_id}/pinned"
    )
    self.logger.info("Pinned the chatroom.")
    return response


def read_message(self, chat_room_id: int, message_id: int):
    self._check_authorization()
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.CHAT_ROOMS_V2}/{chat_room_id}/messages/{message_id}/read",
    )
    self.logger.info("Message has been read.")
    return response


def refresh_chat_rooms(self, from_time: int = None) -> ChatRoomsResponse:
    self._check_authorization()
    params = {}
    if from_time:
        params["from_time"] = from_time
    return self._make_request(
        "GET",
        endpoint=f"{Endpoints.CHAT_ROOMS_V2}/update",
        params=params,
        data_type=ChatRoomsResponse,
    )


def remove_chat_rooms(self, chat_room_ids: List[int]):
    self._check_authorization()
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.CHAT_ROOMS_V2}/mass_destroy",
        payload={"chat_room_ids[]": chat_room_ids},
    )
    self.logger.info(f"Chatrooms have been removed.")
    return response


def report_chat_room(
    self,
    chat_room_id: int,
    opponent_id: int,
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
        endpoint=f"{Endpoints.CHAT_ROOMS_V3}/{chat_room_id}/report",
        payload={
            "chat_room_id": chat_room_id,
            "opponent_id": opponent_id,
            "category_id": category_id,
            "reason": reason,
            "screenshot_filename": screenshot_filename,
            "screenshot_2_filename": screenshot_2_filename,
            "screenshot_3_filename": screenshot_3_filename,
            "screenshot_4_filename": screenshot_4_filename,
        },
    )
    self.logger.info(f"Chatroom '{chat_room_id}' has been reported.")
    return response


def send_message(
    self,
    chat_room_id: int,
    message_type: str,
    call_type: str = None,
    text: str = None,
    font_size: int = None,
    gif_image_id: int = None,
    attachment_file_name: str = None,
    sticker_pack_id: int = None,
    video_file_name: str = None,
) -> MessageResponse:
    self._check_authorization()
    response = self._make_request(
        "POST",
        endpoint=f"{Endpoints.CHAT_ROOMS_V3}/{chat_room_id}/messages/new",
        payload={
            "chat_room_id": chat_room_id,
            "message_type": message_type,
            "call_type": call_type,
            "text": text,
            "font_size": font_size,
            "gif_image_id": gif_image_id,
            "attachment_file_name": attachment_file_name,
            "sticker_pack_id": sticker_pack_id,
            "video_file_name": video_file_name,
        },
        data_type=MessageResponse,
    )
    self.logger.info("Your message has been sent.")
    return response


def unhide_chat(self, chat_room_ids: int):
    self._check_authorization()
    response = self._make_request(
        "DELETE",
        endpoint=f"{Endpoints.HIDDEN_V1}/chats",
        params={"chat_room_ids[]": chat_room_ids},
    )
    self.logger.info("Unhid the chatrooms")
    return response


def unpin_chat(self, chat_room_id: int):
    self._check_authorization()
    response = self._make_request(
        "DELETE", endpoint=f"{Endpoints.CHAT_ROOMS_V1}/{chat_room_id}/pinned"
    )
    self.logger.info("Unpinned the chatroom")
    return response
