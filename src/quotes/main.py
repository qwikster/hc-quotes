import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Form, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import func, select

from quotes import dbutil
from quotes.api.auth import authfail
from quotes.api.auth import router as authrouter
from quotes.bans import dobans
from quotes.config import appdir, config, templates
from quotes.dbutil import DB, ID, USER, get_count, get_hash
from quotes.models.quote import Quote

logger = logging.getLogger("uvicorn.error")

@asynccontextmanager
async def lifespan(app: FastAPI):
    dbutil.create_all()
    yield

def api_routes(app: FastAPI):
    app.include_router(authrouter, prefix="")

    @app.post("/create", status_code=status.HTTP_201_CREATED)
    def create(db: DB, request: Request, user: USER, author: str = Form(..., max_length=64), quote: str = Form(..., max_length=1024)):
        if not author.strip() or not quote.strip():
            raise HTTPException(400, detail = "a field is empty")
        user.total_quotes += 1
        page = Quote(
            id=get_hash(db, len=6),
            author = author,
            quote = quote.replace("\n", " "),
            user = user
        )
        db.add(page)
        db.commit()
        return RedirectResponse(f"/q/{page.id}", status_code=status.HTTP_303_SEE_OTHER)

    @app.post("/vote")
    def vote(request: Request, db: DB, user: USER, up: bool, id: str):
        quote = db.get(Quote, id)
        if not quote or quote.deleted:
            raise(HTTPException(404, detail = "quote not found!"))
        if any(v[0] == user.id for v in quote.votes) and user.id != "1":
            raise(HTTPException(409, detail = "you already voted for this!"))
        quote.votes = quote.votes + [(user.id, up)]
        db.commit()
        dobans(db, quote)

        return({
            "id": quote.id,
            "votes": get_count(quote)
        })

def app_routes(app: FastAPI):
    @app.get("/q/{id}")
    def get_quote(db: DB, user: ID, request: Request, id: str):
        quote = db.get(Quote, id)
        if not quote or quote.deleted:
            return templates.TemplateResponse(
                request = request,
                name = "404.html",
                context = {
                    "path": id
                },
                status_code=404
            )
        return templates.TemplateResponse(
            request = request,
            name = "quote.html",
            context = {
                "id": quote.id,
                "author": quote.author,
                "quote": quote.quote,
                "submitter": quote.user.nickname.capitalize(),
                "votes": get_count(quote),
                "voted": any(v[0] == user.id for v in quote.votes) if user else True,
                "logged_in": bool(user),
            }
        )

    @app.get("/quotes")
    def get_quotes(db: DB, uid: ID, limit: int = 30, offset: int = 0, random: bool = True) -> list[dict]:
        rand = func.random() if random else Quote.created_at.desc()
        stmt = select(Quote).where(Quote.deleted == False).order_by(rand).offset(offset).limit(limit)
        list = db.scalars(stmt).all()

        results = []
        for q in list:
            results.append({
                "id": q.id,
                "author": q.author,
                "quote": q.quote,
                "submitter": q.user.nickname,
                "votes": get_count(q),
                "voted": any(v[0] == uid.id for v in q.votes) if uid else True
            })

        return results

    # HOMEPAGE and css/js
    app.mount("/", StaticFiles(directory=appdir.parent.parent / "static", html = True), name = "frontend")

def create_app() -> FastAPI:
    app = FastAPI(lifespan = lifespan)
    api_routes(app)
    app_routes(app)

    @app.exception_handler(status.HTTP_401_UNAUTHORIZED)
    async def unauthed_handle(request: Request, exc: HTTPException):
        return authfail(request, "You are not logged in!")

    return app

def entry():
    if config().devmode:
        uvicorn.run(
            "quotes.main:create_app",
            host = config().host,
            port = config().port,
            reload = True,
            factory = True,
            log_level = "info"
        )
    else:
        uvicorn.run(
            "quotes.main:create_app",
            host = config().host,
            port = config().port,
            reload = False,
            factory = True,
            log_level = "info"
        )

if __name__ == "__main__":
    entry()


#
# TODO TOMORROW:   ADD DATABASE!!!!!
#
