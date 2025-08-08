from web.server import create_app
from app.config import Settings
from app.bot import TradingBot, EventBus

if __name__ == "__main__":
    settings = Settings.from_env()
    event_bus = EventBus()
    bot = TradingBot(settings, event_bus)
    app = create_app(settings, event_bus, bot)

    # Start bot only if credentials look valid
    if settings.IQ_EMAIL and settings.IQ_PASSWORD:
        bot.start()
        event_bus.publish({"type": "bot_status", "status": "booting", "ts": 0})
    else:
        event_bus.publish({"type": "bot_status", "status": "waiting_credentials", "ts": 0})

    app.run(host=settings.HOST, port=settings.PORT, threaded=True, use_reloader=False)