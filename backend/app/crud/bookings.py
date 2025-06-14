from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import timedelta

from .available_slots import (
    get_available_slot_by_id,
    update_available_slot,
    get_single_slot_with_freelancer_contact,
)
from app.exceptions import exception
from app.models.bookings import Booking, BookingStatus
from app.schema.bookings import BookingCreate, BookingUpdate
from app.schema.available_slots import AvailableSlotUpdate
from app.services.zoom_service import ZoomService
from app.services.email_notification import (
    notify_client_on_booking_request,
    notify_freelancer_on_booking_request,
    notify_client_on_booking_confirmation,
    notify_client_on_booking_cancellation,
)


def create_booking(db: Session, slot_id: int, data: BookingCreate) -> Booking:
    slot = get_single_slot_with_freelancer_contact(db, slot_id)
    if slot.is_booked:
        raise exception.AppException(
            "Slot is already booked", code="slot.already_booked", status_code=400
        )

    new_booking = Booking(
        freelancer_id=slot.freelancer_id,
        slot_id=slot.id,
        time=slot.start_time,
        client_name=data.client_name,
        client_email=data.client_email,
    )

    try:
        db.add(new_booking)
        db.commit()
        db.refresh(new_booking)
        notify_client_on_booking_request(
            client_name=new_booking.client_name,
            client_email=new_booking.client_email,
            freelancer_name=slot.freelancer_name,
            booking_time=new_booking.time,
        )
        notify_freelancer_on_booking_request(
            freelancer_name=slot.freelancer_name,
            freelancer_email=slot.freelancer_email,
            client_name=new_booking.client_name,
            booking_time=new_booking.time,
        )
        return new_booking
    except SQLAlchemyError:
        db.rollback()
        raise exception.AppException(
            "Failed to create booking",
            code="booking.creation_error",
            target="database",
            status_code=500,
        )


def get_booking_by_id(db: Session, booking_id: int) -> Booking:
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise exception.AppException(
            "Booking not found", code="booking.not_found", status_code=404
        )
    return booking


def get_bookings_by_freelancer_id(db: Session, freelancer_id: int) -> list[Booking]:
    bookings = db.query(Booking).filter(Booking.freelancer_id == freelancer_id).all()
    return bookings


def update_booking(
    db: Session, booking_id: int, logged_in_freelancer_id: int, data: BookingUpdate
) -> Booking:
    booking = get_booking_by_id(db, booking_id)

    slot = get_single_slot_with_freelancer_contact(db, booking.slot_id)

    if booking.freelancer_id != logged_in_freelancer_id:
        raise exception.AppException(
            "You do not have permission to update this booking",
            code="booking.permission_denied",
            status_code=403,
        )

    if data.status == booking.status:
        raise exception.AppException(
            "No changes detected in booking status",
            code="booking.no_changes",
            status_code=400,
        )

    if booking.status in (BookingStatus.PENDING, BookingStatus.CONFIRMED):
        if (
            booking.status == BookingStatus.PENDING
            and data.status == BookingStatus.CONFIRMED
        ):
            if slot.is_booked:
                raise exception.AppException(
                    "This slot is already booked",
                    code="slot.already_booked",
                    status_code=400,
                )
            booking.status = BookingStatus.CONFIRMED

            # create zoom meeting
            meeting = ZoomService.create_meeting(
                topic=f"Booking #{booking.id} with {booking.client_name}",
                start_time=slot.start_time,
                duration=60,
            )

            booking.meeting_link = meeting["join_url"]

            time_diff = slot.end_time - slot.start_time

            if time_diff < timedelta(hours=2):
                update_data = AvailableSlotUpdate(is_booked=True)
                print("less than two hours difference", update_data.model_dump())

            else:
                update_data = AvailableSlotUpdate(
                    start_time=slot.start_time + timedelta(hours=1)
                )
                print("more than two hours difference", update_data.model_dump())

            update_available_slot(
                db=db,
                slot_id=slot.id,
                freelancer_id=logged_in_freelancer_id,
                data=update_data,
            )

            notify_client_on_booking_confirmation(
                client_email=booking.client_email,
                client_name=booking.client_name,
                booking_time=booking.time,
                freelancer_name=slot.freelancer_name,
                meeting_link=booking.meeting_link,
            )

        elif (
            booking.status == BookingStatus.PENDING
            and data.status == BookingStatus.CANCELLED
        ):
            booking.status = BookingStatus.CANCELLED
            notify_client_on_booking_cancellation(
                client_email=booking.client_email,
                client_name=booking.client_name,
                booking_time=booking.time,
                freelancer_name=slot.freelancer_name,
            )

        elif booking.status == BookingStatus.CONFIRMED and (
            data.status == BookingStatus.CANCELLED
            or data.status == BookingStatus.COMPLETED
        ):
            booking.status = data.status
            notify_client_on_booking_cancellation(
                client_email=booking.client_email,
                client_name=booking.client_name,
                booking_time=booking.time,
                freelancer_name=slot.freelancer_name,
            )

        else:
            raise exception.AppException(
                "Sorry this operation is not allowed",
                code="booking.operation_not_allowed",
                status_code=400,
            )
    else:
        raise exception.AppException(
            "Completed and cancelled bookings cannot be updated",
            code="booking.operation_not_allowed",
            status_code=400,
        )

    try:
        db.commit()
        db.refresh(booking)
        return booking
    except SQLAlchemyError:
        db.rollback()
        raise exception.AppException(
            "Failed to update booking",
            code="booking.update_error",
            target="database",
            status_code=500,
        )
