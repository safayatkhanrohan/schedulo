from typing import Annotated
from fastapi import Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import SessionLocal
from app.models.freelancer import Freelancer
from app.core.security import decode_access_token
from app.crud.freelancer import get_freelancer_by_id
from app.exceptions import exception


def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError:
        exception.AppException(
            "Internal Server Error: Database operation failed",
            code="database_error",
            status_code=500,
        )
    finally:
        db.close()


async def get_current_user(
    request: Request, db: Session = Depends(get_db)
) -> Freelancer:
    token = request.cookies.get("access_token")

    if not token:
        raise exception.UnAuthenticatedException()

    decoded_token = decode_access_token(token)

    if decoded_token is None:
        raise exception.InvalidTokenException()

    user_id = int(decoded_token)
    user = get_freelancer_by_id(db, user_id)

    if user is None:
        raise exception.InvalidTokenException()

    return user


CurrentUser = Annotated[Freelancer, Depends(get_current_user)]
