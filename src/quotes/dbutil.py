import hashlib
from datetime import UTC, datetime
from typing import Annotated

from fastapi import Cookie, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from quotes.db import Base, engine, get_db
from quotes.models.session import Session as SessionModel
from quotes.models.user import User

DB = Annotated[Session, Depends(get_db)]

def create_all():
    from quotes.models import quote, session, user  # noqa: F401
    Base.metadata.create_all(bind=engine)

def getuser(db: DB, token: Annotated[str | None, Cookie()] = None) -> User:
    if not token:
        raise HTTPException(401)
    hashed = hashlib.sha256(token.encode()).hexdigest()

    stmt = (
        select(User)
        .join(SessionModel)
        .where(
            SessionModel.token_hash == hashed,
            SessionModel.expires_at > datetime.now(UTC)
        )
    )
    user = db.scalar(stmt)
    if user:
        return user

    raise HTTPException(401)

USER = Annotated[User, Depends(getuser)]
