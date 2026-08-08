import hashlib
import secrets
import string
from datetime import UTC, datetime
from typing import Annotated

from fastapi import Cookie, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from quotes.db import Base, engine, get_db
from quotes.models.quote import Quote
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

def getuser_safe(db: DB, token: Annotated[str | None, Cookie()] = None) -> User | None:
    if not token:
        return None
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
    return None

def get_hash(db: DB, len: int = 6) -> str:
    chars = string.ascii_letters + string.digits
    while True:
        hash = "".join(secrets.choice(chars) for _ in range(len))
        exists = db.scalar(
            select(Quote.id).where(Quote.id == hash)
        )
        if not exists:
            return hash

USER = Annotated[User, Depends(getuser)]
ID = Annotated[User | None, Depends(getuser_safe)]
