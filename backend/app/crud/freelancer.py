from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.schema.freelancer import FreelancerCreate
from app.models.freelancer import Freelancer
from app.core.security import verify_password, get_password_hash
from app.exceptions import exception


def get_freelancer_by_id(db: Session, user_id: int) -> Freelancer | None:
    return db.query(Freelancer).filter(Freelancer.id == user_id).first()


def get_freelancer_by_email(db: Session, email: str) -> Freelancer | None:
    return db.query(Freelancer).filter(Freelancer.email == email).first()


def create_freelancer(db: Session, user: FreelancerCreate) -> Freelancer:

    # Check if user with that email already exists
    db_user = get_freelancer_by_email(db, email=user.email)
    if db_user:
        raise exception.UserAlreadyExistsException()

    hashed_password = get_password_hash(user.password.get_secret_value())

    # Create the DB model instance, excluding the plain password
    db_freelancer = Freelancer(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        hashed_password=hashed_password,
    )

    try:
        db.add(db_freelancer)
        db.commit()
        db.refresh(db_freelancer)
        return db_freelancer
    except SQLAlchemyError as e:
        db.rollback()
        raise exception.AppException(
            "Failed to create freelancer",
            code="freelancer.creation_error",
            target="database",
            status_code=500,
        )


def authenticate_user(db: Session, email: str, password: str) -> Freelancer | None:
    user = get_freelancer_by_email(db, email)

    if not user:
        return None

    if not verify_password(str(password), str(user.hashed_password)):
        return None
    return user
