from flask import Flask, Response
import traceback

from app.modules.functions import make_about_page, make_svg_widget

FAVICON_SVG = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'>
<circle fill='#1ED760' cx='50' cy='50' r='50'/>
<path d='M28 38c16-6 35-4 46 3' fill='none' stroke='#000' stroke-width='6' stroke-linecap='round'/>
<path d='M28 52c16-4 31-2 42 3' fill='none' stroke='#000' stroke-width='6' stroke-linecap='round'/>
<path d='M28 66c13-3 26-2 36 3' fill='none' stroke='#000' stroke-width='6' stroke-linecap='round'/>
</svg>"""


def create_app() -> Flask:
    app: Flask = Flask(__name__)

    @app.route("/about")
    def about() -> Response:
        """Display setup instructions as well as the current song."""
        try:
            resp: Response = Response(
                response=make_about_page(),
                mimetype="text/html",
            )
            resp.headers["Cache-Control"] = "s-maxage=1"  # Cache for 1 second
            resp.headers["Access-Control-Allow-Origin"] = "*"  # Allow all origins
            return resp
        except Exception as e:
            error_html = f"""
            <html>
                <body>
                    <h1>Error Loading About Page</h1>
                    <p>An error occurred: {str(e)}</p>
                    <p>Please check your .env configuration and make sure your credentials are correct.</p>
                    <pre>{traceback.format_exc()}</pre>
                </body>
            </html>
            """
            return Response(response=error_html, mimetype="text/html", status=500)

    @app.route("/favicon.ico")
    def favicon() -> Response:
        resp: Response = Response(response=FAVICON_SVG, mimetype="image/svg+xml")
        resp.headers["Cache-Control"] = "public, max-age=86400"
        return resp

    @app.route("/link")
    def link_alias() -> Response:
        """Backward-compatible alias for /about."""
        return about()

    @app.route(rule="/", defaults={"path": ""})
    @app.route(rule="/<path:path>")
    def catch_all(path: str) -> Response:
        """Catch all requests and return the rendered SVG."""
        try:
            resp: Response = Response(
                response=make_svg_widget(),
                mimetype="image/svg+xml",
            )
            resp.headers["Cache-Control"] = "s-maxage=1"  # Cache for 1 second
            resp.headers["Access-Control-Allow-Origin"] = "*"  # Allow all origins
            return resp
        except Exception as e:
            error_svg = f"""
            <svg width="495" height="160" xmlns="http://www.w3.org/2000/svg">
                <rect width="495" height="160" fill="#f8d7da"/>
                <text x="247.5" y="80" text-anchor="middle" fill="#721c24" font-family="Arial" font-size="14">
                    Error: {str(e)[:50]}
                </text>
                <text x="247.5" y="100" text-anchor="middle" fill="#721c24" font-family="Arial" font-size="12">
                    Check console for details
                </text>
            </svg>
            """
            print(f"Error rendering widget: {e}")
            traceback.print_exc()
            return Response(response=error_svg, mimetype="image/svg+xml", status=500)
    
    @app.route("/health")
    def health() -> Response:
        """Health check endpoint."""
        return Response(response="OK", mimetype="text/plain", status=200)

    return app
