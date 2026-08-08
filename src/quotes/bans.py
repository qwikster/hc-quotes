

from quotes.dbutil import DB, USER, get_count
from quotes.models.quote import Quote

BAN_THRESHOLD = 4
BAN_PERCENT = 0.4
DELETE_QUOTE = -2

def dobans(db: DB, user: USER, quote: Quote):
    if get_count(quote) <= DELETE_QUOTE:
        quote.deleted = True
        user.nuked_quotes += 1
        if user.total_quotes <= BAN_THRESHOLD:
            db.commit()
            return
        if user.nuked_quotes / user.total_quotes > BAN_PERCENT:
            user.banned = True
            db.commit()
            return
