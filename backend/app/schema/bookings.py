from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, model_validator, ConfigDict

from app.utils.validators import ValidatorUtils
from app.models.bookings import BookingStatus


class BookingBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BookingCreate(BookingBase):
    client_name: str = Field(..., min_length=1, max_length=100)
    client_email: EmailStr

    @model_validator(mode="after")
    def validate_booking(cls, values):
        ValidatorUtils.validate_name(values.client_name)
        ValidatorUtils.validate_email(values.client_email)
        return values


class BookingUpdate(BaseModel):
    status: Optional[BookingStatus] = None


class BookingResponse(BookingBase):
    id: int = Field(..., ge=1)
    freelancer_id: int = Field(..., ge=1)
    slot_id: int = Field(..., ge=1)
    time: datetime
    meeting_link: Optional[str] = None
    status: BookingStatus = Field(default=BookingStatus.PENDING)
