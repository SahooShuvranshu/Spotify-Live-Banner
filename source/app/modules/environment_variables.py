from os import getenv
from typing import Optional

from dotenv import load_dotenv

from app.modules.paths import PATHS


class ENV_VARS:
    load_dotenv(PATHS.ROOT_DIRECTORY / ".env")

    REFRESH_TOKEN: Optional[str] = getenv("REFRESH_TOKEN")
    CLIENT_ID: Optional[str] = getenv("CLIENT_ID")
    CLIENT_SECRET: Optional[str] = getenv("CLIENT_SECRET")

    if not all({REFRESH_TOKEN, CLIENT_ID, CLIENT_SECRET}):
        raise EnvironmentError("Error obtaining required environment variables.")
