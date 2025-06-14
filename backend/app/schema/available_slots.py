from datetime import datetime
from typing import Optional

from pydantic import BaseModel, model_validator, ConfigDict

from app.utils.validators import ValidatorUtils


class AvailableSlotBase(BaseModel):
    start_time: datetime
    end_time: datetime

    @model_validator(mode="after")
    def validate_time_slot(cls, values):
        ValidatorUtils.validate_time_slot(values.start_time, values.end_time)
        return values

    model_config = ConfigDict(from_attributes=True)


class AvailableSlotCreate(AvailableSlotBase):
    pass


class AvailableSlotUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_booked: Optional[bool] = None

    @model_validator(mode="after")
    def validate_update_times(cls, values):
        start_time = values.start_time
        end_time = values.end_time

        if start_time is not None and end_time is not None:
            ValidatorUtils.validate_time_slot(start_time, end_time)
        return values


class AvailableSlotResponse(AvailableSlotBase):
    id: int
    freelancer_id: int
    is_booked: bool


class SlotResWithFreelancer(AvailableSlotResponse):
    freelancer_name: str
    freelancer_email: str
