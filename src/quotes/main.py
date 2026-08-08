import logging
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
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
    # app.include_router(bnuuy.router, prefix="/api/bnuuy")
    pass

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

    @app.get("/create")
    def abc():
        pass

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
