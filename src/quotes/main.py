import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Form, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from quotes import dbutil
from quotes.api.auth import authfail
from quotes.api.auth import router as authrouter
from quotes.config import appdir, config, templates
from quotes.dbutil import DB, ID, USER, get_hash
from quotes.models.quote import Quote

logger = logging.getLogger("uvicorn.error")

@asynccontextmanager
async def lifespan(app: FastAPI):
    dbutil.create_all()
    yield

def api_routes(app: FastAPI):
    app.include_router(authrouter, prefix="")

    @app.post("/create", status_code=status.HTTP_201_CREATED)
    def create(db: DB, request: Request, user: USER, author: str = Form(...), quote: str = Form(...)):
        print(user.__dict__)
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
    def vote(request: Request, up: bool, id: str):
        votes = 0
        return {"message": f"upvoted {id}!", "votes": votes}

def app_routes(app: FastAPI):
    @app.get("/q/{id}")
    def get_quote(db: DB, user: ID, request: Request, id: str):
        quote = db.get(Quote, id)
        if not quote:
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
                "submitter": quote.user.nickname,
                "quote": quote.quote,
                "votes": len(quote.votes),
                "voted": user and user.id in quote.votes,
                "logged_in": bool(user),
                "author": quote.author,
            }
        )

    @app.get("/quotes")
    def get_quotes() -> list[dict[str, tuple[str, str]]]:
        return [{"quote": ("uid", "quote")}, {}]

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
