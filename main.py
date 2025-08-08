from web.server import create_app
import uvicorn
from app.config import Settings

if __name__ == "__main__":
    settings = Settings.from_env()
    app = create_app(settings)
    uvicorn.run(app, host=settings.HOST, port=settings.PORT, reload=False, log_level="info")