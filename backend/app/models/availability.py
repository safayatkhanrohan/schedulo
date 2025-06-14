from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey
from app.db.base import Base
from sqlalchemy.orm import relationship, validates


class AvailableSlot(Base):
    __tablename__ = "available_slots"

    id = Column(Integer, primary_key=True, index=True)
    freelancer_id = Column(
        Integer, ForeignKey("freelancers.id", ondelete="CASCADE"), nullable=False
    )
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    is_booked = Column(Boolean, default=False, nullable=False)

    # Relationships
    freelancer = relationship("Freelancer", back_populates="available_slots")
    booking = relationship(
        "Booking", back_populates="slot", uselist=False, cascade="all, delete-orphan"
    )

    
