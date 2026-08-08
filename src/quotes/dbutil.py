from quotes.db import Base, engine


def create_all():
    from quotes.models import quote, session, user  # noqa: F401
    Base.metadata.create_all(bind=engine)
