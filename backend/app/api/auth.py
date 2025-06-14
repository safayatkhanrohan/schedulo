from fastapi import APIRouter, Response, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.deps.deps import get_db, CurrentUser
from app.crud.freelancer import authenticate_user, create_freelancer
from app.core.security import create_access_token
from app.core.config import settings
from app.schema.freelancer import FreelancerGet, FreelancerCreate
from app.exceptions.exception import InvalidCredentialsException
from app.schema.response import SuccessResponse
from app.schema.auth import LoginRequest

router = APIRouter()


@router.post(
    "/signup",
    response_model=SuccessResponse[FreelancerGet],
    status_code=status.HTTP_201_CREATED,
)
async def signup_user(user: FreelancerCreate, db: Session = Depends(get_db)):
    user = create_freelancer(db, user)

    return SuccessResponse(
        data=user,
        message="User created successfully",
    )


@router.post(
    "/login", response_model=SuccessResponse[None], status_code=status.HTTP_200_OK
)
async def login(
    response: Response,
    form_data: LoginRequest,
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db, email=form_data.email, password=form_data.password.get_secret_value()
    )

    if not user:
        raise InvalidCredentialsException()

    # create jwt with user_id
    access_token = create_access_token(str(user.id))
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=True,  # Set to True if using HTTPS
    )

    return SuccessResponse(
        data=None,
        message="Login successful",
    )


@router.get("/me", response_model=FreelancerGet, status_code=status.HTTP_200_OK)
def read_current_freelancer(current_user: CurrentUser):
    return current_user


@router.post(
    "/logout", response_model=SuccessResponse[None], status_code=status.HTTP_200_OK
)
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="lax",
        secure=True,  # Ensure this matches your cookie settings
    )
    return SuccessResponse(
        data=None,
        message="Logout successful",
    )
