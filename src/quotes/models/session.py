from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from quotes.db import Base, timestamp
from quotes.models.user import User


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True, index = True)
    token_hash: Mapped[str] = mapped_column(unique = True, index = True)
    created_at: Mapped[timestamp]
    expires_at: Mapped[datetime] = mapped_column(DateTime)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index = True)
    user: Mapped["User"] = relationship()
