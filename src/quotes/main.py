import logging
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from quotes import dbutil
from quotes.api.auth import router as authrouter
from quotes.config import appdir, config, templates

logger = logging.getLogger("uvicorn.error")

@asynccontextmanager
async def lifespan(app: FastAPI):
    dbutil.create_all()
    yield

def api_routes(app: FastAPI):
    app.include_router(authrouter, prefix="")

    @app.post("/create", status_code=status.HTTP_201_CREATED)
    def create(request: Request, author: str, quote: str):
        id = ""
        return templates.TemplateResponse(
            request = request,
            name = "200.html",
            context = {
                "id": "beans",
            }
        )

    @app.post("/vote")
    def vote(request: Request, up: bool, id: str):
        votes = 0
        return {"message": f"upvoted {id}!", "votes": votes}

def app_routes(app: FastAPI):
    @app.get("/quote/{id}")
    def get_quote(request: Request, id: str):
        return templates.TemplateResponse(
            request = request,
            name = "quote.html",
            context = {
                "submitter_nick": "qwik",
                "quote": "cheese",
                "votes": "0",
                "author_nick": "zach latta",
                "author_id": "slackidhere"
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
