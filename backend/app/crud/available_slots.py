from sqlalchemy import func, literal
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.schema.available_slots import (
    AvailableSlotCreate,
    AvailableSlotUpdate,
    SlotResWithFreelancer,
)
from app.models.availability import AvailableSlot
from app.models.freelancer import Freelancer
from app.exceptions import exception
from app.crud.freelancer import get_freelancer_by_id


def create_available_slot(
    db: Session, data: AvailableSlotCreate, freelancer_id: int
) -> AvailableSlot:
    overlapping_slot = (
        db.query(AvailableSlot)
        .filter(
            AvailableSlot.freelancer_id == freelancer_id,
            AvailableSlot.end_time > data.start_time,
            AvailableSlot.start_time < data.end_time,
        )
        .first()
    )
    if overlapping_slot:
        raise exception.TimeSlotConflictException()

    new_slot = AvailableSlot(
        freelancer_id=freelancer_id,
        start_time=data.start_time,
        end_time=data.end_time,
        is_booked=False,
    )

    try:
        db.add(new_slot)
        db.commit()
        db.refresh(new_slot)
        return new_slot
    except SQLAlchemyError as e:
        db.rollback()
        raise exception.AppException(
            message="Failed to create available slot",
            code="slot.creation_error",
            target="database",
            status_code=500,
        )


def get_available_slots(db: Session, freelancer_id: int) -> list[AvailableSlot]:
    # Ensure the freelancer exists
    freelancer = get_freelancer_by_id(db, freelancer_id)
    if not freelancer:
        raise exception.AppException(
            message="Freelancer not found",
            code="freelancer.not_found",
            target="freelancer_id",
            status_code=404,
        )

    slots = (
        db.query(AvailableSlot)
        .filter(AvailableSlot.freelancer_id == freelancer_id)
        .all()
    )

    return slots


def get_available_slot_by_id(db: Session, slot_id: int) -> AvailableSlot:
    slot = db.query(AvailableSlot).filter(AvailableSlot.id == slot_id).first()
    if not slot:
        raise exception.AppException(
            message="Available slot not found",
            code="slot.not_found",
            target="slot_id",
            status_code=404,
        )
    return slot


def get_single_slot_with_freelancer_contact(
    db: Session, slot_id: int
) -> SlotResWithFreelancer:
    row = (
        db.query(
            AvailableSlot,
            func.concat(
                Freelancer.first_name, literal(" "), Freelancer.last_name
            ).label("freelancer_name"),
            Freelancer.email.label("freelancer_email"),
        )
        .join(Freelancer, AvailableSlot.freelancer_id == Freelancer.id)
        .filter(AvailableSlot.id == slot_id)
        .first()
    )
    if not row:
        raise exception.AppException(
            message="Available slot not found",
            code="slot.not_found",
            target="slot_id",
            status_code=404,
        )
    slot, freelancer_name, freelancer_email = row
    slot.freelancer_name = freelancer_name
    slot.freelancer_email = freelancer_email

    return slot


def update_available_slot(
    db: Session, slot_id: int, freelancer_id: int, data: AvailableSlotUpdate
) -> AvailableSlot:

    slot = (
        db.query(AvailableSlot)
        .filter(
            AvailableSlot.id == slot_id,
        )
        .first()
    )

    if not slot:
        raise exception.AppException(
            message="Available slot not found",
            code="slot.not_found",
            target="slot_id",
            status_code=404,
        )

    if slot.freelancer_id != freelancer_id:
        raise exception.AppException(
            message="You do not have permission to update this slot",
            code="slot.permission_denied",
            target="freelancer_id",
            status_code=403,
        )

    # Only validate overlap if both start and end times are provided
    if data.start_time and data.end_time:
        overlapping_slot = (
            db.query(AvailableSlot)
            .filter(
                AvailableSlot.freelancer_id == freelancer_id,
                AvailableSlot.id != slot_id,
                AvailableSlot.end_time > data.start_time,
                AvailableSlot.start_time < data.end_time,
            )
            .first()
        )

        if overlapping_slot:
            raise exception.TimeSlotConflictException()

    # Update only if fields are present
    if data.start_time is not None:
        slot.start_time = data.start_time
    if data.end_time is not None:
        slot.end_time = data.end_time
    if data.is_booked is not None:
        slot.is_booked = data.is_booked
    try:

        db.commit()
        db.refresh(slot)
        return slot

    except SQLAlchemyError as e:
        db.rollback()
        raise exception.AppException(
            message="Failed to update available slot",
            code="slot.update_error",
            target="database",
            status_code=500,
        )


def delete_available_slot(db: Session, slot_id: int, freelancer_id: int) -> None:
    slot = (
        db.query(AvailableSlot)
        .filter(
            AvailableSlot.id == slot_id,
            AvailableSlot.freelancer_id == freelancer_id,  # enforce ownership
        )
        .first()
    )

    if not slot:
        raise exception.AppException(
            message="Available slot not found",
            code="slot.not_found",
            target="slot_id",
            status_code=404,
        )
    try:
        db.delete(slot)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise exception.AppException(
            message="Failed to delete available slot",
            code="slot.deletion_error",
            target="database",
            status_code=500,
        )
