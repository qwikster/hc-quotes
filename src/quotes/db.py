import datetime
from typing import Annotated

from sqlalchemy import DateTime, create_engine, func
from sqlalchemy.orm import DeclarativeBase, mapped_column, sessionmaker

from quotes.config import config

engine = create_engine(
    config().db_url,
    connect_args={"check_same_thread": False},
    echo=config().devmode
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

timestamp = Annotated[
    datetime.datetime,
    mapped_column(DateTime(timezone=True), server_default=func.now())
]
