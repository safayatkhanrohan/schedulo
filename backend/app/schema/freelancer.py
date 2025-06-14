from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator, SecretStr, ConfigDict
from app.utils.validators import ValidatorUtils


class FreelancerBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50, examples=["John"])
    last_name: str = Field(..., min_length=1, max_length=50, examples=["Doe"])
    email: EmailStr = Field(..., examples=["johndoe@example.com"])

    @field_validator("first_name", "last_name")
    def validate_name(cls, v: str) -> str:
        return ValidatorUtils.validate_name(v)

    @field_validator("email")
    def validate_email(cls, v: EmailStr) -> EmailStr:
        ValidatorUtils.validate_email(v)
        return v

    model_config = ConfigDict(from_attributes=True)


class FreelancerCreate(FreelancerBase):
    password: SecretStr = Field(
        ...,
        min_length=8,
        max_length=128,
        examples=["NewPass456@"],
    )

    @field_validator("password")
    def validate_password(cls, v: SecretStr) -> SecretStr:
        ValidatorUtils.validate_password(v.get_secret_value())
        return v


class FreelancerGet(FreelancerBase):
    id: int = Field(..., ge=1, example=1)


class FreelancerUpdate(FreelancerBase):  # Now inherits from base
    # All fields become optional through overrides
    first_name: Optional[str] = Field(
        None, min_length=1, max_length=50, examples=["Jane"]
    )
    last_name: Optional[str] = Field(
        None, min_length=1, max_length=50, examples=["Smith"]
    )
    email: Optional[EmailStr] = Field(None, examples=["janesmith@example.com"])
    password: Optional[SecretStr] = Field(
        None, min_length=8, max_length=128, examples=["NewPass456@"]
    )

    # Special handling for optional password validation
    @field_validator("password")
    def password_validator(cls, v):
        if v is not None:
            ValidatorUtils.validate_password(v.get_secret_value())
        return v
