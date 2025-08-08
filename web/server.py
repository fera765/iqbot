from __future__ import annotations
import json
import queue
from pathlib import Path
from flask import Flask, Response, render_template, request, jsonify, stream_with_context
from app.config import Settings
from app.bot import TradingBot, EventBus


def create_app(settings: Settings, event_bus: EventBus, bot: TradingBot) -> Flask:
    base_dir = Path(__file__).resolve().parent
    static_dir = str(base_dir / "static")
    templates_dir = str(base_dir / "templates")

    app = Flask(__name__, static_folder=static_dir, template_folder=templates_dir)

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/events")
    def events():
        try:
            limit = int(request.args.get("limit", 100))
        except Exception:
            limit = 100
        return jsonify(event_bus.get_latest(limit))

    @app.get("/catalog")
    def catalog():
        return jsonify(bot.latest_catalog)

    @app.get("/stream")
    def stream():
        client_queue: queue.Queue = queue.Queue(maxsize=1000)

        def handler(evt):
            try:
                client_queue.put_nowait(evt)
            except Exception:
                pass

        event_bus.subscribe(handler)

        def gen():
            try:
                yield "data: {}\n\n"
                while True:
                    evt = client_queue.get()
                    yield f"data: {json.dumps(evt)}\n\n"
            except GeneratorExit:
                event_bus.unsubscribe(handler)

        headers = {
            "Content-Type": "text/event-stream",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
        return Response(stream_with_context(gen()), headers=headers)

    return app