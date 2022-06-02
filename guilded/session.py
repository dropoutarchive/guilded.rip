import uuid, random
import requests, sys, os
from .hashing import Hashing

class Session:

    def __init__(self, proxy: dict = None):
        self._base_url = "https://www.guilded.gg/api"
        self._session = requests.Session()
        if proxy != None: self._session.proxies.update(proxy)

        self._session.headers.update({
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "content-type": "application/json",
            "cookie": "gk=show_team_explore_native%2Cuser_trust_score%2Cvideo_streaming_pip_view_enabled%2Cshow_team_discovery%2Cadd_external_bots%2Cstream_camera_and_capture%2Cstream_simulcast_disabled%2Cnative_streaming%2Cshow_game_presence%2Clinux_desktop_app_download; ",
            "guilded-client-id": str(uuid.uuid4()),
            "guilded-stag": "unset",
            "origin": "https://www.guilded.gg",
            "referer": "https://google.com/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        })

        self.is_ratelimited = False
        self.user = None

    @staticmethod
    def random_string(lenght: int):
        return os.urandom(lenght)[:lenght]

    def login(self, username: str, password: str):
        payload = {
            "email": username,
            "getMe": True,
            "password": password
        }
        response = self._session.post("%s/login" % (self._base_url), json=payload)
        cookies = response.cookies
        response = response.json()

        if response.get("code") == None:
            self.token_login(cookies.get("hmac_signed_session"))
            self.user = response["user"]
            return {
                "error": False,
                "message": "Successfully logged in.",
                "data": {
                    "response": response,
                    "mid": cookies.get("guilded_mid"),
                    "hmac_signed_session": cookies.get("hmac_signed_session")
                }
            }
        else:
            return {
                "error": True,
                "message": response.get("message")
            }

    def token_login(self, token: str):
        self._session.headers["cookie"] += "hmac_signed_session=%s; " % (token)

    def register(self, register_type: str, **kwargs):
        if register_type == "username":
            payload = {
                "username": kwargs.get("username"),
                "extraInfo": {
                    "platform": sys.platform
                }
            }
        else:
            payload = {
                "email": kwargs.get("email"),
                "extraInfo": {
                    "platform": sys.platform
                },
                "fullName": kwargs.get("full_name"),
                "name": kwargs.get("name"),
                "password": kwargs.get("password")
            }

        for value in payload.items():
            if value[1] == None:
                return {
                    "error": True,
                    "message": "\"%s\" can't be none" % (value[0])
                }

        self._session.headers["guilded-stag"] = Hashing.stag(kwargs.get("name") if register_type == "email" else kwargs.get("username"))
        response = self._session.post("%s/users?type=%s" % (self._base_url, register_type), json=payload).json()

        if response.get("user") != None:
            self.user = response["user"]
            return {
                "error": False,
                "message": "Successfully registered account.",
                "data": {
                    "response": response
                }
            }
        else:
            return {
                "error": True,
                "code": response.get("code"),
                "message": response.get("message")
            }

    def join(self, invite: str):
        response = self._session.put("%s/invites/%s" % (self._base_url, invite)).json()

        if response.get("teamId") != None:
            return {
                "error": False,
                "message": "Successfully joined guild.",
                "data": {
                    "response": response
                }
            }
        else:
            return {
                "error": True,
                "code": response.get("code"),
                "message": response.get("message")
            }

    def send_message(self, channel_id: str, message: str, confirmed: bool = False, silent: bool = False, private: bool = False, replies: list = []):
        payload = {
            "messageId": str(uuid.uuid1()),
            "content": {
                "object": "value",
                "document": {
                    "object": "document",
                    "data": {},
                    "nodes": [
                        {
                            "object": "block",
                            "type": "paragraph",
                            "data": {},
                            "nodes": [
                                {
                                    "object": "text",
                                    "leaves": [
                                        {
                                            "object": "leaf",
                                            "text": message,
                                            "marks": []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            },
            "repliesToIds": replies,
            "confirmed": confirmed,
            "isSilent": silent,
            "isPrivate": private
        }
        response = self._session.post("%s/channels/%s/messages" % (self._base_url, channel_id), json=payload).json()
        
        if response.get("message") != None:
            return {
                "error": False,
                "message": "Successfully sent message.",
                "data": {
                    "response": response
                }
            }
        else:
            return {
                "error": True,
                "code": response.get("code"),
                "message": response.get("message")
            }

    def add_user(self, ids: list):
        response = self._session.post("%s/users/me/friendrequests" % (self._base_url), json={
            "friendUserIds": ids
        })

        if response.status_code == 200:
            return {
                "error": False,
                "message": "Successfully sent message.",
                "data": {
                    "response": response.json()
                }
            }
        else:
            return {
                "error": True,
                "code": response.json().get("code"),
                "message": response.json().get("message")
            }

    def email_verified(self):
        response = self._session.get("%s/users/me/verification" % (self._base_url)).json()

        if response.get("email") == True:
            return {
                "error": False,
                "message": "User is email verified.",
                "data": {
                    "response": response
                }
            }
        else:
            return {
                "error": True,
                "message": "User is not email verified.",
                "data": {
                    "response": response
                }
            }

    def ping(self):
        self._session.put("%s/users/me/ping" % (self._base_url), json={})

    def set_status(self, status: int = 1):
        # Online = 1
        # Idle = 2
        # Dnd = 3
        # Offline = 4
        
        response = self._session.post("%s/users/me/presence" % (self._base_url), json={"status": status})
        if response.status_code == 200:
            return {
                "error": False,
                "message": "Successfully updated status.",
                "data": {
                    "response": response
                }
            }
        else:
            return {
                "error": True,
                "message": "User is not email verified.",
                "data": {
                    "response": response
                }
            }

    def set_custom_status(self, status: str, reaction_id: int = 90002547):
        payload = {
            "content":{
                "object": "value",
                "document": {
                    "object": "document",
                    "data": {
                        
                    },
                    "nodes": [
                        {
                        "object": "block",
                        "type": "paragraph",
                        "data": {
                            
                        },
                        "nodes": [
                            {
                                "object": "text",
                                "leaves":[
                                    {
                                    "object": "leaf",
                                    "text": status,
                                    "marks":[
                                        
                                    ]
                                    }
                                ]
                            }
                        ]
                        }
                    ]
                }
            },
            "customReactionId": reaction_id,
            "expireInMs": 0
        }
        
        response = self._session.post("%s/users/me/status" % (self._base_url), json=payload)
        if response.status_code == 200:
            return {
                "error": False,
                "message": "Successfully updated status.",
                "data": {
                    "response": response.json()
                }
            }
        else:
            return {
                "error": True,
                "code": response.json().get("code"),
                "message": response.json().get("message")
            }

    def set_bio(self, content: list, user_id: str = None):
        if user_id == None: user_id = self.user.get("id")
        if user_id == None:
            return {
                "error": True,
                "message": "Please provide the users ID."
            }

        response = self._session.put("%s/users/%s/profilev2" % (self._base_url, user_id), json={
            "userId": user_id,
            "aboutInfo": {"tagLine": content}
        })

        if response.status_code == 200:
            return {
                "error": False,
                "message": "Successfully updated bio.",
                "data": {
                    "response": response.json()
                }
            }
        else:
            return {
                "error": True,
                "code": response.json().get("code"),
                "message": response.json().get("message")
            }

    def add_profile_picture(self, url: str):
        response = self._session.post("%s/users/me/profile/images" % (self._base_url), json={
            "imageUrl": url
        })

        if response.status_code == 200:
            return {
                "error": False,
                "message": "Successfully updated the profile picture.",
                "data": {
                    "response": response.json()
                }
            }
        else:
            return {
                "error": True,
                "code": response.json().get("code"),
                "message": response.json().get("message")
            }
