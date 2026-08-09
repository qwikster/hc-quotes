from typing import TYPE_CHECKING

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from quotes.db import Base, timestamp

if TYPE_CHECKING:
    from quotes.models.user import User


class Quote(Base):
    __tablename__ = "quotes"

    id: Mapped[str] = mapped_column(unique = True, primary_key = True)
    deleted: Mapped[bool] = mapped_column(default = False)
    created_at: Mapped[timestamp]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    user: Mapped["User"] = relationship(back_populates = "quotes")
    author: Mapped[str]
    quote: Mapped[str]
    votes: Mapped[list[tuple[int, bool]]] = mapped_column(JSON, default = list)
    score: Mapped[int] = mapped_column(default=0, index=True)
