from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from quotes.db import Base, timestamp

if TYPE_CHECKING:
    from quotes.models.quote import Quote


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement = True, unique = True, index = True)
    created_at: Mapped[timestamp]
    slack_id: Mapped[str] = mapped_column(unique = True)
    email: Mapped[str] = mapped_column(unique = True)
    hca_ident: Mapped[str] = mapped_column(unique = True)
    nickname: Mapped[str]

    quotes: Mapped[list["Quote"]] = relationship(back_populates = "user")
    total_quotes: Mapped[int] = mapped_column(default = 0)
    nuked_quotes: Mapped[int] = mapped_column(default = 0)
    banned: Mapped[bool] = mapped_column(default = False)
