from sqlalchemy import Column, Integer, String
from app.db.base import Base
from sqlalchemy.orm import relationship, validates
from app.utils.validators import ValidatorUtils

class Freelancer(Base):
    __tablename__ = "freelancers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False, index=True)
    last_name = Column(String(50), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)

    # Relationships
    available_slots = relationship(
        "AvailableSlot", back_populates="freelancer", cascade="all, delete-orphan"
    )
    bookings = relationship(
        "Booking", back_populates="freelancer", cascade="all, delete-orphan"
    )
