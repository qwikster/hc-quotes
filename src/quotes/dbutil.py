from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from quotes.db import Base, engine, get_db


def create_all():
    from quotes.models import quote, session, user  # noqa: F401
    Base.metadata.create_all(bind=engine)

DB = Annotated[Session, Depends(get_db)]
