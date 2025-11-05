import os
from app import create_app


app = create_app()

if __name__ == "__main__":
    # Get port from environment variable (for cloud hosting) or use 8080 for testing
    port = int(os.environ.get("PORT", 8080))
    
    # Check if running in production (common environment variables used by hosting platforms)
    is_production = os.environ.get("FLASK_ENV") == "production" or \
                   os.environ.get("RAILWAY_ENVIRONMENT") is not None or \
                   os.environ.get("RENDER") is not None or \
                   os.environ.get("VERCEL") is not None or \
                   os.environ.get("DYNO") is not None  # Heroku
    
    if not is_production:
        print("=" * 60)
        print("🎵 Spotify Live Banner - Development Server")
        print("=" * 60)
        print()
        print(f"⚠️  WARNING: This should be deployed to cloud!")
        print(f"   For production deployment, see: QUICK_DEPLOY.md")
        print()
        print(f"Development server at: http://127.0.0.1:{port}")
        print(f"Widget: http://127.0.0.1:{port}/")
        print(f"Link page: http://127.0.0.1:{port}/link")
        print(f"Health: http://127.0.0.1:{port}/health")
        print()
        print("Press Ctrl+C to stop")
        print("=" * 60)
        print()
    
    # Run with appropriate settings based on environment
    if is_production:
        # Production mode: no debug, bind to 0.0.0.0 to accept external connections
        app.run(debug=False, host='0.0.0.0', port=port)
    else:
        # Development mode: enable debug, bind to localhost only
        # WARNING: This is for testing only. Deploy to cloud for production use!
        app.run(debug=True, host='127.0.0.1', port=port)
