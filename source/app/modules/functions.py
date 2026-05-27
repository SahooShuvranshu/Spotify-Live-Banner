from base64 import b64encode
from collections import OrderedDict
from io import BytesIO
from random import randint
from time import sleep, time
from typing import Any, Callable, Dict, Union, Optional, Tuple, List, cast

from flask import render_template, request
from PIL import Image
from requests import get, post, Response
from requests.exceptions import RequestException
from werkzeug.datastructures import MultiDict

from app.modules.base64 import BASE_64
from app.modules.colors import COLORS
from app.modules.environment_variables import ENV_VARS
from app.modules.parsed_arguments import ParsedArgs, PROVIDER


HTTP_TIMEOUT_SECONDS = 8
REQUEST_RETRIES = 2
RETRY_BACKOFF_SECONDS = 0.5
CACHE_TTL_SECONDS = 300
CACHE_MAX_ITEMS = 256

BASE64_CACHE: "OrderedDict[str, Tuple[float, str]]" = OrderedDict()
COLOR_CACHE: "OrderedDict[str, str]" = OrderedDict()


def get_cached_base64(cache_key: str) -> Optional[str]:
    cached = BASE64_CACHE.get(cache_key)
    if not cached:
        return None
    cached_at, value = cached
    if time() - cached_at > CACHE_TTL_SECONDS:
        BASE64_CACHE.pop(cache_key, None)
        return None
    BASE64_CACHE.move_to_end(cache_key)
    return value


def set_cached_base64(cache_key: str, value: str) -> None:
    BASE64_CACHE[cache_key] = (time(), value)
    BASE64_CACHE.move_to_end(cache_key)
    while len(BASE64_CACHE) > CACHE_MAX_ITEMS:
        BASE64_CACHE.popitem(last=False)


def request_with_retry(request_fn: Callable[[], Response]) -> Response:
    last_error: Optional[RequestException] = None
    for attempt in range(REQUEST_RETRIES):
        try:
            response = request_fn()
            response.raise_for_status()
            return response
        except RequestException as exc:
            last_error = exc
            if attempt < REQUEST_RETRIES - 1:
                sleep(RETRY_BACKOFF_SECONDS * (2 ** attempt))
            else:
                raise
    if last_error:
        raise last_error
    raise RuntimeError("Request failed without an error.")


def response_json_object(response: Response) -> Dict[str, Any]:
    data = response.json()
    if not isinstance(data, dict):
        raise ValueError("Unexpected response payload.")
    return data


class SpotifyAPI:
    def __init__(self, client_id: str, client_secret: str, refresh_token: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token

    def get_token(self) -> str:
        """Get a new access token."""
        response = request_with_retry(
            lambda: post(
                url="https://accounts.spotify.com/api/token",
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": self.refresh_token,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
                timeout=HTTP_TIMEOUT_SECONDS,
            )
        )
        token_data = response_json_object(response)
        access_token = token_data.get("access_token")
        if not isinstance(access_token, str):
            raise ValueError("Spotify access token missing.")
        return access_token

    def make_request(self, endpoint: str) -> Dict[str, Any]:
        """Make a request to the specified Spotify endpoint."""
        token = self.get_token()
        response = request_with_retry(
            lambda: get(
                url=f"https://api.spotify.com/v1/{endpoint}",
                headers={
                    "Authorization": f"Bearer {token}",
                },
                timeout=HTTP_TIMEOUT_SECONDS,
            )
        )
        return {} if response.status_code == 204 else response_json_object(response)


class LastFMAPI:
    def __init__(self, api_key: str, username: str):
        self.api_key = api_key
        self.username = username

    def get_recent_tracks(self) -> Dict[str, Any]:
        """Get the most recent tracks for the user."""
        params: Dict[str, str] = {
            "method": "user.getrecenttracks",
            "user": self.username,
            "api_key": self.api_key,
            "format": "json",
            "limit": "1",
        }
        response = request_with_retry(
            lambda: get(
                url="https://ws.audioscrobbler.com/2.0/",
                params=params,
                timeout=HTTP_TIMEOUT_SECONDS,
            )
        )
        return response_json_object(response)


class ImageLoader:
    @staticmethod
    def extract_dominant_color(image_data: bytes) -> str:
        """Extract the dominant color from image bytes."""
        try:
            img = Image.open(BytesIO(image_data))
            # Resizing to 1x1 to get average color
            img_small = img.resize((1, 1), resample=Image.Resampling.LANCZOS)
            res = img_small.getpixel((0, 0))

            if isinstance(res, int):  # Grayscale
                return f"{res:02x}{res:02x}{res:02x}"
            if isinstance(res, tuple) and len(res) >= 3:
                r, g, b = res[:3]
                return f"{r:02x}{g:02x}{b:02x}"
            return COLORS.SPOTIFY_GREEN
        except Exception:
            return COLORS.SPOTIFY_GREEN

    @staticmethod
    def load_base_64_image_from_url(image_url: str) -> str:
        """Get the Base64 encoded image from url."""
        cache_key = f"image:{image_url}"
        cached = get_cached_base64(cache_key)
        if cached:
            return cached
        response = request_with_retry(
            lambda: get(image_url, timeout=HTTP_TIMEOUT_SECONDS)
        )
        encoded = b64encode(response.content).decode("ascii")
        set_cached_base64(cache_key, encoded)

        # Pre-cache color while we have the content
        if image_url not in COLOR_CACHE:
            COLOR_CACHE[image_url] = ImageLoader.extract_dominant_color(response.content)
            while len(COLOR_CACHE) > CACHE_MAX_ITEMS:
                COLOR_CACHE.popitem(last=False)

        return encoded

    @staticmethod
    def get_color_from_url(image_url: str) -> str:
        """Get the dominant color from an image url."""
        if image_url in COLOR_CACHE:
            return COLOR_CACHE[image_url]

        # If not cached, we need to fetch it
        try:
            response = request_with_retry(
                lambda: get(image_url, timeout=HTTP_TIMEOUT_SECONDS)
            )
            color = ImageLoader.extract_dominant_color(response.content)
            COLOR_CACHE[image_url] = color
            return color
        except Exception:
            return COLORS.SPOTIFY_GREEN


class WidgetGenerator:
    @staticmethod
    def generate_eq_bars_html(bar_count: int, eq_color: str, is_playing: bool = True) -> str:
        """Build the HTML/CSS snippets for the equalizer bars to be injected."""
        css: str = ""
        if eq_color == "rainbow":
            css += ".bar-container { animation-duration: 2s; }"
        for i in range(bar_count):
            random_duration: int = randint(500, 750)
            background_color: str = (
                COLORS.SPECTRUM[i] if eq_color == "rainbow" else eq_color
            )
            if is_playing:
                animation_style = f"animation-duration: {random_duration}ms;"
            else:
                animation_style = "animation: none !important; transform: scaleY(0.5); opacity: 1;"
            
            css += f""".bar:nth-child({i + 1}) {{
                {animation_style}
                background: #{background_color};
            }}"""
        bar_html: str = "<div class='bar'></div>"
        eq_bars_html: str = "".join([bar_html for _ in range(bar_count)])
        return f"""
            {eq_bars_html}
            <style>{css}</style>
        """


def parse_request_args(request_args: MultiDict[str, str]) -> ParsedArgs:
    """Parse the request args into a ParsedArgs object."""
    parsed_request_args: Dict[str, Any] = ParsedArgs.parse_request_args(request_args)
    return ParsedArgs(**parsed_request_args)

def get_spotify_track(spotify_api: SpotifyAPI, recently_playing: bool = False) -> Optional[Dict[str, Any]]:
    """Get the currently playing track from Spotify, with optional fallback to recently played."""
    now_playing: Dict[str, Any] = spotify_api.make_request(
        "me/player/currently-playing"
    )
    
    now_playing_track = now_playing.get("item")
    is_active = now_playing.get("is_playing", False)

    # If something is playing, return it
    if now_playing_track and is_active:
        return now_playing_track  # type: ignore[no-any-return]

    # If nothing is playing and we don't want history, return None (Not Listening)
    if not recently_playing:
        return None

    # Fallback to recently played if requested
    recently_played: Dict[str, Any] = spotify_api.make_request(
        "me/player/recently-played?limit=1"
    )
    items: List[Dict[str, Any]] = recently_played.get("items", [])
    if not items:
        return None
    
    # Strictly return the track dictionary or None
    track_item = items[0].get("track")
    if isinstance(track_item, dict):
        return track_item
    return None


def normalize_lastfm_track(track: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize Last.fm track data to a Spotify-like shape."""
    artist_data = track.get("artist", {})
    artist_name = ""
    if isinstance(artist_data, dict):
        artist_name = artist_data.get("#text") or artist_data.get("name") or ""
    elif isinstance(artist_data, str):
        artist_name = artist_data

    image_url = ""
    images: List[Dict[str, str]] = track.get("image", [])
    if isinstance(images, list):
        for image in reversed(images):
            if image.get("#text"):
                image_url = image["#text"]
                break

    album_images = []
    if image_url:
        album_images = [{"url": image_url}, {"url": image_url}, {"url": image_url}]

    return {
        "name": track.get("name", "No Track Playing"),
        "artists": [{"name": artist_name or "Last.fm"}],
        "album": {"images": album_images},
        "id": None,
        "uri": None,
        "external_urls": {"lastfm": track.get("url")},
    }


def get_lastfm_track(lastfm_api: LastFMAPI, recently_playing: bool = False) -> Optional[Dict[str, Any]]:
    """Get the track from Last.fm, optionally falling back to the most recent one."""
    data = lastfm_api.get_recent_tracks()
    tracks = data.get("recenttracks", {}).get("track", [])
    if isinstance(tracks, dict):
        tracks = [tracks]
    if not tracks:
        return None

    first_track = tracks[0]
    # Check if the track is currently playing
    is_now_playing = first_track.get("@attr", {}).get("nowplaying") == "true"
    if not is_now_playing and not recently_playing:
        return None

    return normalize_lastfm_track(first_track)


def get_track_with_provider(provider: PROVIDER, recently_playing: bool = False) -> Tuple[Dict[str, Any], str]:
    """Get a track from Spotify, falling back to Last.fm."""
    spotify_error: Optional[Exception] = None
    lastfm_error: Optional[Exception] = None
    spotify_track: Optional[Dict[str, Any]] = None

    if provider == PROVIDER.SPOTIFY:
        if not ENV_VARS.has_spotify():
            raise EnvironmentError("Missing Spotify credentials.")
        spotify_api = SpotifyAPI(
            client_id=ENV_VARS.CLIENT_ID or "",
            client_secret=ENV_VARS.CLIENT_SECRET or "",
            refresh_token=ENV_VARS.REFRESH_TOKEN or "",
        )
        spotify_track = get_spotify_track(spotify_api, recently_playing)
        return (spotify_track or {}), "spotify"

    if provider == PROVIDER.LASTFM:
        if not ENV_VARS.has_lastfm():
            raise EnvironmentError("Missing Last.fm credentials.")
        lastfm_api = LastFMAPI(
            api_key=ENV_VARS.LASTFM_API_KEY or "",
            username=ENV_VARS.LASTFM_USERNAME or "",
        )
        track = get_lastfm_track(lastfm_api, recently_playing)
        return (track or {}), "lastfm"

    if ENV_VARS.has_spotify():
        try:
            spotify_api = SpotifyAPI(
                client_id=ENV_VARS.CLIENT_ID or "",
                client_secret=ENV_VARS.CLIENT_SECRET or "",
                refresh_token=ENV_VARS.REFRESH_TOKEN or "",
            )
            spotify_track = get_spotify_track(spotify_api, recently_playing)
            if spotify_track:
                return spotify_track, "spotify"
        except RequestException as exc:
            spotify_error = exc

    if ENV_VARS.has_lastfm():
        try:
            lastfm_api = LastFMAPI(
                api_key=ENV_VARS.LASTFM_API_KEY or "",
                username=ENV_VARS.LASTFM_USERNAME or "",
            )
            track = get_lastfm_track(lastfm_api, recently_playing)
            return (track or {}), "lastfm"
        except RequestException as exc:
            lastfm_error = exc

    if spotify_track is not None:
        return {}, "spotify"

    if spotify_error or lastfm_error:
        raise RuntimeError("Unable to fetch track from Spotify or Last.fm.")

    raise EnvironmentError(
        "Missing credentials: set Spotify or Last.fm environment variables."
    )


def get_base_64_track_image(track: Dict[str, Any], is_playing: bool = True) -> str:
    """Get the Base64 encoded image from a track or the logo if not playing."""
    images = track.get("album", {}).get("images", [])
    if images and is_playing:
        album_image_url: str = images[min(1, len(images) - 1)]["url"]
        return ImageLoader.load_base_64_image_from_url(album_image_url)
    return BASE_64.SPOTIFY_LOGO


def get_base_64_scan_code(spotify_uri: str, background: str, foreground: str) -> str:
    """Get the track (scan) code for a song in Base64."""
    try:
        scan_code_url = f"https://scannables.scdn.co/uri/plain/png/{background}/{foreground}/500/{spotify_uri}"
        return ImageLoader.load_base_64_image_from_url(scan_code_url)
    except RequestException:
        return BASE_64.PLACEHOLDER_SCAN_CODE


def prepare_widget_template_variables(
    parsed_args: ParsedArgs, track: Dict[str, Any], provider: str
) -> Dict[str, Union[str, bool]]:
    # Handle case where no track data is available
    is_playing = bool(track)
    if not track:
        track = {
            "name": "Not Listening Anything",
            "artists": [{"name": "Spotify" if provider == "spotify" else "Last.fm"}],
            "uri": "spotify:track:default",
            "album": {"images": []}
        }

    # Extract dynamic color if adaptive is true
    eq_color = parsed_args.eq_color
    dominant_color = None
    if parsed_args.adaptive and is_playing:
        images = track.get("album", {}).get("images", [])
        if images:
            adaptive_url: str = images[min(1, len(images) - 1)]["url"]
            # This ensures both b64 and color are cached
            ImageLoader.load_base_64_image_from_url(adaptive_url)
            dominant_color = ImageLoader.get_color_from_url(adaptive_url)
            eq_color = dominant_color

    eq_bars_html = WidgetGenerator.generate_eq_bars_html(
        parsed_args.bar_count, eq_color, is_playing=is_playing
    )
    track_name = track.get("name", "Unknown Track")
    track_artist = track.get("artists", [{}])[0].get("name", "Unknown Artist")
    base_64_track_image = get_base_64_track_image(track, is_playing=is_playing)
    spotify_uri = track.get("uri") if provider == "spotify" else None
    if parsed_args.scan and spotify_uri and is_playing:
        base_64_scan_code = get_base_64_scan_code(
            spotify_uri,
            parsed_args.scan_color_background,
            parsed_args.scan_color_foreground,
        )
    else:
        base_64_scan_code = ""
    spin = parsed_args.spin if is_playing else False
    logo = BASE_64.SPOTIFY_LOGO
    
    # Text Color and Background Logic
    title_color = parsed_args.title_color
    subtitle_color = parsed_args.subtitle_color
    background_color = parsed_args.main_background_color

    # If we have an adaptive background (Glass + Adaptive OR Blur), calculate contrast
    if dominant_color and (parsed_args.theme.value == "glass" or parsed_args.blur):
        r = int(dominant_color[0:2], 16)
        g = int(dominant_color[2:4], 16)
        b = int(dominant_color[4:6], 16)
        
        # Update background if in glass theme
        if parsed_args.theme.value == "glass":
            background_color = f"rgba({r}, {g}, {b}, 0.5)"
        
        # Perceived brightness formula
        brightness = (r * 299 + g * 587 + b * 114) / 1000
        if brightness > 140: # Light background -> Dark text
            title_color = COLORS.BLACK
            subtitle_color = "rgba(0, 0, 0, 0.7)"
        else: # Dark background -> Light text
            title_color = COLORS.WHITE
            subtitle_color = "rgba(255, 255, 255, 0.7)"
    
    # Final Color Formatting for CSS
    if len(title_color) == 6 and not any(c in title_color for c in "(#,"):
        title_color = f"#{title_color}"
        
    if len(subtitle_color) == 6 and not any(c in subtitle_color for c in "(#,"):
        subtitle_color = f"#{subtitle_color}"
        
    if len(background_color) == 6 and not any(c in background_color for c in "(#,"):
        background_color = f"#{background_color}"

    return {
        "eq_bars_html": eq_bars_html,
        "track_name": track_name,
        "track_artist": track_artist,
        "base_64_track_image": base_64_track_image,
        "base_64_scan_code": base_64_scan_code,
        "is_playing": is_playing,
        "spin": spin,
        "blur": parsed_args.blur,
        "logo": logo,
        "provider": provider,
        "title_color": title_color,
        "subtitle_color": subtitle_color,
        "background_color": background_color,
        "theme": parsed_args.theme.value
    }


def make_svg_widget() -> str:
    """Returns the HTML of the widget to be rendered."""
    parsed_args = parse_request_args(request.args)
    track, provider = get_track_with_provider(
        parsed_args.provider, parsed_args.recently_playing
    )
    template_variables = prepare_widget_template_variables(
        parsed_args, track, provider
    )
    return render_template("widget.html", **template_variables)


def make_about_page() -> str:
    """Returns the HTML of the about page to be rendered."""
    parsed_args = parse_request_args(request.args)

    query_string = request.query_string.decode("utf-8")
    banner_url = f"/?{query_string}" if query_string else "/"
    base_url = request.host_url.rstrip("/")
    banner_abs_url = f"{base_url}{banner_url}"
    return render_template(
        "about.html",
        banner_url=banner_url,
        banner_abs_url=banner_abs_url,
        base_url=base_url,
        page_url=request.url,
    )
