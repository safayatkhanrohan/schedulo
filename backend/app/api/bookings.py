from fastapi import APIRouter, Query, status, Depends
from sqlalchemy.orm import Session

from app.crud.bookings import (
    create_booking,
    update_booking,
    get_bookings_by_freelancer_id,
    get_booking_by_id,
)
from app.schema.bookings import BookingCreate, BookingResponse, BookingUpdate
from app.deps.deps import get_db, CurrentUser
from app.schema.response import SuccessResponse
router = APIRouter()


@router.get(
    "/",
    response_model=SuccessResponse[list[BookingResponse]],
    status_code=status.HTTP_200_OK,
)
def get_logged_in_freelancer_bookings(
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    """
    Get all bookings for the logged-in freelancer.
    """
    bookings = get_bookings_by_freelancer_id(db=db, freelancer_id=current_user.id)

    return SuccessResponse(data=bookings, message="Bookings retrieved successfully")


@router.get(
    "/{booking_id}",
    response_model=SuccessResponse[BookingResponse],
    status_code=status.HTTP_200_OK,
)
def get_single_booking(
    booking_id: int,
    db: Session = Depends(get_db),
):
    booking = get_booking_by_id(db=db, booking_id=booking_id)

    return SuccessResponse(data=booking, message="Booking retrieved successfully")


@router.post(
    "/create",
    response_model=SuccessResponse[BookingResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_booking_endpoint(
    booking_data: BookingCreate,
    slot_id: int = Query(
        ..., ge=1, description="ID of the available slot being booked"
    ),
    db: Session = Depends(get_db),
):
    # booking = create_booking( booking_data)
    booking = create_booking(db=db, slot_id=slot_id, data=booking_data)
    return SuccessResponse(data=booking, message="Booking created successfully")


@router.put(
    "/update/{booking_id}",
    response_model=SuccessResponse[BookingResponse],
    status_code=status.HTTP_200_OK,
)
def update_booking_endpoint(
    current_user: CurrentUser,
    booking_id: int,
    booking_data: BookingUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a booking's status.
    Only the freelancer who created the booking can update it.
    """
    updated_booking = update_booking(
        db=db,
        booking_id=booking_id,
        logged_in_freelancer_id=current_user.id,
        data=booking_data,
    )
    return SuccessResponse(data=updated_booking, message="Booking updated successfully")
