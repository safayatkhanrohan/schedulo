from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.deps.deps import get_db, CurrentUser
from app.schema.response import SuccessResponse
from app.schema.available_slots import (
    AvailableSlotCreate,
    AvailableSlotResponse,
    AvailableSlotUpdate,
)
from app.crud.available_slots import (
    create_available_slot,
    get_available_slots,
    update_available_slot,
    delete_available_slot,
    get_available_slot_by_id,
)

router = APIRouter()


@router.post(
    "/",
    response_model=SuccessResponse[AvailableSlotResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_availability(
    current_user: CurrentUser,
    data: AvailableSlotCreate,
    db: Session = Depends(get_db),
):
    if not current_user:
        return
    new_slot = create_available_slot(db=db, data=data, freelancer_id=current_user.id)

    return SuccessResponse(
        data=new_slot,
        message="Available slot created successfully",
    )


@router.get(
    "/{slot_id}",
    response_model=SuccessResponse[AvailableSlotResponse],
    status_code=status.HTTP_200_OK,
)
def get_single_available_slot(slot_id: int, db: Session = Depends(get_db)):
    slot = get_available_slot_by_id(db=db, slot_id=slot_id)
    return SuccessResponse(data= slot, message="Slot feteched Successfully")


@router.get(
    "/freelancer/{freelancer_id}",
    response_model=SuccessResponse[list[AvailableSlotResponse]],
    status_code=status.HTTP_200_OK,
)
def get_availability(
    freelancer_id: int,
    db: Session = Depends(get_db),
):

    slots = get_available_slots(db=db, freelancer_id=freelancer_id)
    return SuccessResponse(
        data=slots,
        message="Available slots retrieved successfully",
    )


@router.put(
    "/{slot_id}",
    response_model=SuccessResponse[AvailableSlotResponse],
    status_code=status.HTTP_200_OK,
)
def update_availability(
    current_user: CurrentUser,
    slot_id: int,
    data: AvailableSlotUpdate,
    db: Session = Depends(get_db),
):
    updated_slot = update_available_slot(
        db=db, slot_id=slot_id, data=data, freelancer_id=current_user.id
    )

    return SuccessResponse(
        data=updated_slot,
        message="Available slot updated successfully",
    )


@router.delete(
    "/{slot_id}",
    response_model=SuccessResponse[None],
    status_code=status.HTTP_200_OK,
)
def delete_availability(
    current_user: CurrentUser,
    slot_id: int,
    db: Session = Depends(get_db),
):
    delete_available_slot(db=db, slot_id=slot_id, freelancer_id=current_user.id)

    return SuccessResponse(
        data=None,
        message="Available slot deleted successfully",
    )
