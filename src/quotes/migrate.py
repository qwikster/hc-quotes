#WARNING: DO NOT USE THIS FFILE UNLESS YOU KNOW WHAT THIS DOES

from quotes.db import get_db
from quotes.dbutil import DB, get_count
from quotes.models.quote import Quote

db = next(get_db())

quotes = db.query(Quote).all()
for q in quotes:
    q.score = get_count(q)
db.commit()
db.close()
