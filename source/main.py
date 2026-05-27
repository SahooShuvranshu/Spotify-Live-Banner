import os
from app import create_app


app = create_app()

if __name__ == "__main__":
    # Get port from environment variable (for cloud hosting) or use 8080 for testing
    port = int(os.environ.get("PORT", 8080))
    use_dev_server = os.environ.get("DEV_SERVER") == "1" or os.environ.get("FLASK_DEBUG") == "1"

    if use_dev_server:
        print("=" * 60)
        print("🎵 Spotify Live Banner - Development Server")
        print("=" * 60)
        print()
        print(f"Development server at: http://127.0.0.1:{port}")
        print(f"Widget: http://127.0.0.1:{port}/")
        print(f"About page: http://127.0.0.1:{port}/about")
        print(f"Health: http://127.0.0.1:{port}/health")
        print()
        print("Press Ctrl+C to stop")
        print("=" * 60)
        print()
        app.run(debug=True, host="127.0.0.1", port=port)
    else:
        print("=" * 60)
        print("🎵 Spotify Live Banner - Production Server")
        print("=" * 60)
        print()
        print(f"Server at: http://127.0.0.1:{port}")
        print(f"Widget: http://127.0.0.1:{port}/")
        print(f"About page: http://127.0.0.1:{port}/about")
        print(f"Health: http://127.0.0.1:{port}/health")
        print()
        print("Set DEV_SERVER=1 to use Flask's debug server.")
        print("=" * 60)
        print()
        os.execvp(
            "gunicorn",
            [
                "gunicorn",
                "main:app",
                "--bind",
                f"0.0.0.0:{port}",
                "--workers",
                "2",
                "--timeout",
                "120",
            ],
        )
