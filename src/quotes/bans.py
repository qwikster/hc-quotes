from quotes.dbutil import DB, get_count
from quotes.models.quote import Quote

BAN_THRESHOLD = 4
BAN_PERCENT = 0.4
DELETE_QUOTE = -2

def dobans(db: DB, quote: Quote):
    if get_count(quote) <= DELETE_QUOTE:
        quote.deleted = True
        quote.user.nuked_quotes += 1
        if quote.user.total_quotes <= BAN_THRESHOLD:
            db.commit()
            return
        if quote.user.nuked_quotes / quote.user.total_quotes > BAN_PERCENT:
            quote.user.banned = True
            db.commit()
            return
