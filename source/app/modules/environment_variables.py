from os import getenv
from typing import Optional

from dotenv import load_dotenv

from app.modules.paths import PATHS


class ENV_VARS:
    load_dotenv(PATHS.ROOT_DIRECTORY / ".env")

    REFRESH_TOKEN: Optional[str] = getenv("REFRESH_TOKEN")
    CLIENT_ID: Optional[str] = getenv("CLIENT_ID")
    CLIENT_SECRET: Optional[str] = getenv("CLIENT_SECRET")
    LASTFM_API_KEY: Optional[str] = getenv("LASTFM_API_KEY")
    LASTFM_USERNAME: Optional[str] = getenv("LASTFM_USERNAME")

    @classmethod
    def has_spotify(cls) -> bool:
        return all({cls.REFRESH_TOKEN, cls.CLIENT_ID, cls.CLIENT_SECRET})

    @classmethod
    def has_lastfm(cls) -> bool:
        return all({cls.LASTFM_API_KEY, cls.LASTFM_USERNAME})
