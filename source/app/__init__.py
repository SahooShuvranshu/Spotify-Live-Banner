from flask import Flask, Response
import traceback

from app.modules.functions import make_link_page, make_svg_widget


def create_app() -> Flask:
    app: Flask = Flask(__name__)

    @app.route("/link")
    def link() -> Response:
        """Display setup instructions as well as the current song."""
        try:
            resp: Response = Response(
                response=make_link_page(),
                mimetype="text/html",
            )
            resp.headers["Cache-Control"] = "s-maxage=1"  # Cache for 1 second
            resp.headers["Access-Control-Allow-Origin"] = "*"  # Allow all origins
            return resp
        except Exception as e:
            error_html = f"""
            <html>
                <body>
                    <h1>Error Loading Link Page</h1>
                    <p>An error occurred: {str(e)}</p>
                    <p>Please check your .env configuration and make sure your Spotify credentials are correct.</p>
                    <pre>{traceback.format_exc()}</pre>
                </body>
            </html>
            """
            return Response(response=error_html, mimetype="text/html", status=500)

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
