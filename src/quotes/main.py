import logging
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

DEVMODE = True
HOST = "0.0.0.0"
PORT = 1984

logger = logging.getLogger("uvicorn.error")
appdir = Path(__file__).resolve().parent
templates = Jinja2Templates(directory="templates")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Base.metadata.create_all(bind=engine) # ADD THIS
    yield

def api_routes(app: FastAPI):
    @app.post("/create", status_code=status.HTTP_201_CREATED)
    def create(request, author: str, quote: str):
        return {"message": f"created quote {id}!"}

    @app.post("/vote")
    def vote(request, up: bool, id: str):
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
    app.mount("/", StaticFiles(directory="static", html = True), name = "frontend")

def create_app() -> FastAPI:
    app = FastAPI(lifespan = lifespan)
    api_routes(app)
    app_routes(app)
    return app


def entry():
    if DEVMODE:
        uvicorn.run(
            "quotes.main:create_app",
            host = HOST,
            port = PORT,
            reload = True,
            factory = True,
            log_level = "info"
        )
    else:
        uvicorn.run(
            "quotes.main:create_app",
            host = HOST,
            port = PORT,
            reload = False,
            factory = True,
            log_level = "info"
        )

if __name__ == "__main__":
    entry()
