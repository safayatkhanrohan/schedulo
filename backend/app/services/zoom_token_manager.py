import time
import requests
from base64 import b64encode
from app.core.config import settings  # adjust path as needed


class ZoomTokenManager:
    _access_token = None
    _expires_at = 0

    @classmethod
    def get_token(cls) -> str:
        current_time = int(time.time())

        if cls._access_token and current_time < cls._expires_at:
            return cls._access_token

        # Fetch new token
        auth_string = f"{settings.ZOOM_CLIENT_ID}:{settings.ZOOM_CLIENT_SECRET}"
        auth_bytes = b64encode(auth_string.encode()).decode()

        headers = {
            "Authorization": f"Basic {auth_bytes}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        response = requests.post(
            f"https://zoom.us/oauth/token?grant_type=account_credentials&account_id={settings.ZOOM_ACCOUNT_ID}",
            headers=headers,
        )

        if response.status_code != 200:
            raise Exception("Failed to get Zoom token", response.text)

        token_data = response.json()
        cls._access_token = token_data["access_token"]
        cls._expires_at = current_time + token_data["expires_in"] - 60  # 60s buffer

        return cls._access_token
