from __future__ import annotations
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncio
from typing import List
from app.config import Settings
from app.bot import TradingBot, EventBus


class WebSocketManager:
    def __init__(self, event_bus: EventBus) -> None:
        self.active: List[WebSocket] = []
        self.event_bus = event_bus
        self.queue: asyncio.Queue = asyncio.Queue()
        self._started = False

    def start(self):
        if not self._started:
            loop = asyncio.get_event_loop()
            self.event_bus.subscribe(lambda e: loop.call_soon_threadsafe(self.queue.put_nowait, e))
            self._started = True

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active:
            self.active.remove(websocket)

    async def broadcaster(self):
        while True:
            event = await self.queue.get()
            dead = []
            for ws in self.active:
                try:
                    await ws.send_json(event)
                except Exception:
                    dead.append(ws)
            for d in dead:
                self.disconnect(d)


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(title="IQOption MHI Bot")
    app.mount("/static", StaticFiles(directory="web/static"), name="static")
    templates = Jinja2Templates(directory="web/templates")

    event_bus = EventBus()
    bot = TradingBot(settings, event_bus)
    ws_manager = WebSocketManager(event_bus)

    def _has_valid_credentials() -> bool:
        return (
            settings.IQ_EMAIL and settings.IQ_PASSWORD and
            "seu_email@" not in settings.IQ_EMAIL and settings.IQ_PASSWORD != "sua_senha"
        )

    @app.on_event("startup")
    async def _startup():
        ws_manager.start()
        asyncio.create_task(ws_manager.broadcaster())
        if _has_valid_credentials():
            bot.start()
        else:
            event_bus.publish({
                "type": "bot_status",
                "status": "waiting_credentials",
                "message": "Edite o arquivo .env com IQ_EMAIL e IQ_PASSWORD válidos para iniciar o bot.",
                "ts": 0
            })

    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})

    @app.get("/events")
    async def events(limit: int = 100):
        return bot.event_bus.get_latest(limit)

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await ws_manager.connect(websocket)
        try:
            while True:
                await websocket.receive_text()  # keep alive / ignored
        except WebSocketDisconnect:
            ws_manager.disconnect(websocket)

    return app