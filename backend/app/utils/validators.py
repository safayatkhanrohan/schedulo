import re
from datetime import timedelta

class ValidatorUtils:

    @staticmethod
    def validate_name(name: str) -> str:
        pattern = r"^[a-zA-Z\s\-\.]{1,50}$" # only letters, spaces, hyphens, and periods
        if not re.match(pattern, name):
            raise ValueError("Invalid name format. Only letters, spaces, hyphens, and periods are allowed.")
        return name.strip()

    @staticmethod
    def validate_email(email: str) -> str:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, email):
            raise ValueError("Invalid email address")
        return email

    @staticmethod
    def validate_password(password: str) -> str:
        if (
            len(password) < 8
            or not any(c.isupper() for c in password)
            or not any(c.isdigit() for c in password)
            or not any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?/" for c in password)
            or not any(c.islower() for c in password)
        ):
            raise ValueError(
                "Password must be at least 8 characters long and include uppercase and lowercase letters, a number, and a special character."
            )
        return password

    @staticmethod
    def validate_time_slot(start_time, end_time):
        if end_time <= start_time:
            raise ValueError("End time must be after start time")

        # Check for at least 1 hour difference
        if end_time - start_time < timedelta(hours=1):
            raise ValueError(
                "There must be at least a 1 hour difference between start and end time"
            )
        return start_time, end_time
