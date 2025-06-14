import requests
from app.services.zoom_token_manager import ZoomTokenManager
from datetime import datetime


class ZoomService:
    @staticmethod
    def create_meeting(topic: str, start_time: datetime, duration: int = 50):
        token = ZoomTokenManager.get_token()

        print("Creating Zoom meeting with token:", token)

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        data = {
            "topic": topic,
            "type": 2,
            "start_time": start_time.isoformat(),
            "duration": duration,
            "timezone": "Asia/Dhaka",
            "settings": {
                "host_video": True,
                "participant_video": True,
                "join_before_host": False,
                "mute_upon_entry": True,
            },
        }

        try:
            response = requests.post(
                "https://api.zoom.us/v2/users/me/meetings", headers=headers, json=data
            )
        except requests.RequestException as e:
            raise Exception("Zoom API request failed", str(e))

        if response.status_code != 201:
            raise Exception("Zoom meeting creation failed", response.text)

        return response.json()
