import time
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import sys

from app.core.config import settings


DATABASE_URL = settings.DATABASE_URL
MAX_RETRIES = 7
RETRY_INTERVAL = 2  # seconds

for attempt in range(1, MAX_RETRIES + 1):

    try:
        engine = create_engine(DATABASE_URL)
        # test the connection
        with engine.connect() as connection:
            print("Database connection established.")
        break
    except OperationalError as e:
        print(f"[Attempt {attempt}] Database not ready yet: {e}")
        time.sleep(RETRY_INTERVAL)
else:
    raise RuntimeError("Could not connect to the database after multiple attempts.")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
