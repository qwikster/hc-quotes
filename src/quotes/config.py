from pathlib import Path

from fastapi.templating import Jinja2Templates
from pydantic_settings import BaseSettings, SettingsConfigDict

_config = None
appdir = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=appdir.parent.parent / "templates")

class Config(BaseSettings):
    devmode: bool = False

    hca_id: str | None = None
    hca_secret: str | None = None
    hca_uri: str | None = None

    host: str = "0.0.0.0"
    port: int = 1984
    db_url: str = "sqlite:///quotes.db"

    model_config = SettingsConfigDict(env_file = appdir.parent.parent / ".env", env_file_encoding="utf-8")

def config() -> Config:
    global _config
    if _config is None:
        _config = Config()
    return _config
