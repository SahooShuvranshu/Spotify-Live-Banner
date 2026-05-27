from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict

from werkzeug.datastructures import MultiDict

from app.modules.colors import COLORS


class THEME(Enum):
    LIGHT = "light"
    DARK = "dark"
    GLASS = "glass"


class PROVIDER(Enum):
    AUTO = "auto"
    SPOTIFY = "spotify"
    LASTFM = "lastfm"


class CONSTANTS:
    HEX_CODE_LENGTH: int = 6
    MIN_WIDGET_WIDTH: int = 400  # Unused for now but will be used in the future
    MAX_WIDGET_WIDTH: int = 800  # Unused for now but will be used in the future


@dataclass(frozen=True)
class ParsedArgs:
    spin: bool = False
    scan: bool = False
    recently_playing: bool = False
    adaptive: bool = False
    blur: bool = False
    theme: THEME = THEME.LIGHT
    eq_color: str = COLORS.SPOTIFY_GREEN
    width: int = 500  # Unused for now but will be used in the future
    provider: PROVIDER = PROVIDER.AUTO

    @property
    def main_background_color(self) -> str:
        if self.theme == THEME.LIGHT:
            return COLORS.GITHUB_LIGHT
        elif self.theme == THEME.DARK:
            return COLORS.GITHUB_DARK
        elif self.theme == THEME.GLASS:
            return "rgba(31, 41, 55, 0.7)"  # Dark grey glass
        return COLORS.GITHUB_LIGHT

    @property
    def scan_color_background(self) -> str:
        if self.theme in {THEME.LIGHT, THEME.GLASS}:
            return COLORS.BLACK
        else:
            return COLORS.WHITE

    @property
    def scan_color_foreground(self) -> str:
        # The scannables.scdn.co API requires a text color
        if self.theme == THEME.LIGHT:
            return "white"
        else:
            return "black"

    @property
    def title_color(self) -> str:
        if self.theme == THEME.LIGHT:
            return COLORS.BLACK
        else:
            return COLORS.WHITE

    @property
    def subtitle_color(self) -> str:
        if self.theme == THEME.GLASS:
            return "#94a3b8"
        return COLORS.GREY

    @property
    def bar_count(self) -> int:
        return 10 if self.scan else 12

    @staticmethod
    def is_truhty(value: str) -> bool:
        return value.lower() in {
            "true",
            "1",
            "yes",
            "on",
        }

    @staticmethod
    def parse_request_args(request_args: MultiDict[str, str]) -> Dict[str, Any]:
        return {
            "spin": ParsedArgs.is_truhty(
                request_args.get("spin", "false", type=str)
            ),
            "scan": ParsedArgs.is_truhty(
                request_args.get("scan", "false", type=str)
            ),
            "recently_playing": ParsedArgs.is_truhty(
                request_args.get("recently_playing", "false", type=str)
            ),
            "adaptive": ParsedArgs.is_truhty(
                request_args.get("adaptive", "false", type=str)
            ),
            "blur": ParsedArgs.is_truhty(
                request_args.get("blur", "false", type=str)
            ),
            "theme": THEME(
                request_args.get("theme", THEME.LIGHT.value, type=str)
            ),
            "eq_color": request_args.get(
                "eq_color", COLORS.SPOTIFY_GREEN, type=str
            ),
            "width": request_args.get(
                "width", CONSTANTS.MAX_WIDGET_WIDTH, type=int
            ),
            "provider": PROVIDER(
                request_args.get("provider", PROVIDER.AUTO.value, type=str)
            ),
        }

    def __post_init__(self) -> None:
        self._validate_spin()
        self._validate_scan()
        self._validate_recently_playing()
        self._validate_adaptive()
        self._validate_blur()
        self._validate_theme()
        self._validate_eq_color()
        self._validate_width()
        self._validate_provider()

    def _validate_spin(self) -> None:
        if not isinstance(self.spin, bool):
            raise ValueError("`spin` must be of type `bool`.")

    def _validate_scan(self) -> None:
        if not isinstance(self.scan, bool):
            raise ValueError("`scan` must be of type `bool`.")

    def _validate_recently_playing(self) -> None:
        if not isinstance(self.recently_playing, bool):
            raise ValueError("`recently_playing` must be of type `bool`.")

    def _validate_adaptive(self) -> None:
        if not isinstance(self.adaptive, bool):
            raise ValueError("`adaptive` must be of type `bool`.")

    def _validate_blur(self) -> None:
        if not isinstance(self.blur, bool):
            raise ValueError("`blur` must be of type `bool`.")

    def _validate_theme(self) -> None:
        if self.theme not in THEME:
            raise ValueError("`theme` must be an instance of `THEME`.")

    def _validate_eq_color(self) -> None:
        if not isinstance(self.eq_color, str):
            raise ValueError("`eq_color` must be of type `str`.")
        if (
            self.eq_color != "rainbow"
            and len(self.eq_color) != CONSTANTS.HEX_CODE_LENGTH
        ):
            raise ValueError(
                "`eq_color` must be a valid hex color code of length 6 without a leading `#`."
            )

    def _validate_width(self) -> None:
        if not isinstance(self.width, int):
            raise ValueError("`width`must be of type `int`.")
        if not (CONSTANTS.MIN_WIDGET_WIDTH <= self.width <= CONSTANTS.MAX_WIDGET_WIDTH):
            raise ValueError(
                f"Width must be ∈ [{CONSTANTS.MIN_WIDGET_WIDTH}, {CONSTANTS.MAX_WIDGET_WIDTH}]."
            )

    def _validate_provider(self) -> None:
        if self.provider not in PROVIDER:
            raise ValueError("`provider` must be an instance of `PROVIDER`.")
