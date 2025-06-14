from datetime import datetime
from enum import Enum
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Enum as SQLAlchemyEnum,
)
from app.db.base import Base
from sqlalchemy.orm import relationship, validates


class BookingStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    freelancer_id = Column(
        Integer, ForeignKey("freelancers.id", ondelete="CASCADE"), nullable=False
    )
    slot_id = Column(
        Integer, ForeignKey("available_slots.id", ondelete="CASCADE"), nullable=False
    )
    time = Column(DateTime, default=datetime.utcnow, nullable=False)
    client_name = Column(String(100), nullable=False)
    client_email = Column(String(255), nullable=False)
    meeting_link = Column(String(500))
    status = Column(
        SQLAlchemyEnum(BookingStatus), default=BookingStatus.PENDING, nullable=False
    )

    # Relationships
    freelancer = relationship("Freelancer", back_populates="bookings")
    slot = relationship("AvailableSlot", back_populates="booking")