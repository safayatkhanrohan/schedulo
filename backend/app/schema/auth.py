from pydantic import BaseModel, EmailStr, Field, field_validator, SecretStr
from app.utils.validators import ValidatorUtils

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., examples=["johndoe@example.com"])
    password: SecretStr = Field(..., examples=["StrongPass123!"])

    @field_validator("email")
    def validate_email(cls, v: EmailStr) -> EmailStr:
        ValidatorUtils.validate_email(v)
        return v

    @field_validator("password")
    def validate_password(cls, v: SecretStr) -> SecretStr:
        ValidatorUtils.validate_password(v.get_secret_value())
        return v
