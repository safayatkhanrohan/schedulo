from fastapi import FastAPI
import sys
from app.db.session import engine
from app.db.base import Base
from app.api import (
    auth as routes_auth,
    availability as routes_availability,
    bookings as routes_bookings,
)
from app.core.handlers import register_exception_handlers

try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print("schema creation failed:", e)
    sys.exit(1)

app = FastAPI()
register_exception_handlers(app)  # global error handlers

app.include_router(routes_auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(
    routes_availability.router, prefix="/api/v1/availability", tags=["Availability"]
)
app.include_router(routes_bookings.router, prefix="/api/v1/bookings", tags=["Bookings"])
