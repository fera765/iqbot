from __future__ import annotations
import json
import queue
import threading
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path

from flask import Flask, Response, jsonify, request, render_template, stream_with_context
from colorama import Fore, Style, init as colorama_init

from iqoptionapi.stable_api import IQ_Option
import pandas as pd

colorama_init(autoreset=True)
logger = logging.getLogger("catalog_web")
logger.setLevel(logging.INFO)


class EventBus:
    def __init__(self) -> None:
        self._subs = []
        self._lock = threading.Lock()
        self._latest: List[dict] = []

    def publish(self, evt: dict) -> None:
        et = evt.get("type", "evt")
        if et == "error":
            print(Fore.RED + f"{evt}")
        else:
            print(Style.DIM + f"{evt}")
        with self._lock:
            subs = list(self._subs)
            self._latest.append(evt)
            self._latest = self._latest[-500:]
        for s in subs:
            try:
                s(evt)
            except Exception:
                pass

    def subscribe(self, cb) -> None:
        with self._lock:
            self._subs.append(cb)

    def unsubscribe(self, cb) -> None:
        with self._lock:
            self._subs = [x for x in self._subs if x != cb]

    def latest(self, limit: int = 100) -> List[dict]:
        with self._lock:
            return self._latest[-limit:]


class CatalogService:
    def __init__(self, email: str, password: str, assets: List[str], timeframe: int) -> None:
        self.email = email
        self.password = password
        self.assets = assets
        self.timeframe = timeframe
        self.api: Optional[IQ_Option] = None
        self.bus = EventBus()
        self._lock = threading.Lock()
        self._running = False
        self.results: Dict[str, dict] = {}

    def connect(self) -> None:
        self.api = IQ_Option(self.email, self.password)
        self.api.connect()
        if not self.api.check_connect():
            raise RuntimeError("Falha na conexão com IQ Option")
        self.api.change_balance('PRACTICE')
        self.bus.publish({"type": "status", "message": "Conectado"})

    def fetch_candles(self, asset: str, end_time: datetime, days: int) -> List[dict]:
        all_candles = []
        seen_ids = set()
        current_end = int(end_time.timestamp())
        start_ts = int((end_time - timedelta(days=days)).timestamp())
        max_calls = (24 * (60 // self.timeframe) * days // 1000) + 5
        for _ in range(max_calls):
            chunk = self.api.get_candles(asset, self.timeframe * 60, 1000, current_end)  # type: ignore
            if not chunk:
                break
            current_end = chunk[0]['from'] - 1
            for c in reversed(chunk):
                if c['from'] >= start_ts and c['id'] not in seen_ids:
                    all_candles.insert(0, c)
                    seen_ids.add(c['id'])
            if all_candles and all_candles[0]['from'] <= start_ts:
                break
        return [c for c in all_candles if c['from'] >= start_ts]

    def build_df(self, candles: List[dict]) -> Optional[pd.DataFrame]:
        if not candles:
            return None
        df = pd.DataFrame(candles)
        df['timestamp'] = pd.to_datetime(df['from'], unit='s')
        df.set_index('timestamp', inplace=True)
        df.sort_index(inplace=True)
        df['color'] = df.apply(lambda c: 'GREEN' if c['close'] > c['open'] else ('RED' if c['close'] < c['open'] else 'DOJI'), axis=1)
        return df

    def run_catalog(self, signal_day: datetime, lookback_days: int = 15) -> None:
        with self._lock:
            if self._running:
                raise RuntimeError("Já em execução")
            self._running = True
        try:
            if self.api is None:
                self.connect()
            end_date = signal_day.replace(hour=0, minute=0, second=0, microsecond=0)
            self.bus.publish({"type": "status", "message": f"Coletando candles M{self.timeframe}"})
            per_asset: Dict[str, pd.DataFrame] = {}
            for asset in self.assets:
                candles = self.fetch_candles(asset, end_date, lookback_days)
                df = self.build_df(candles)
                if df is not None:
                    per_asset[asset] = df
                    self.bus.publish({"type": "asset_loaded", "asset": asset, "rows": len(df)})
                else:
                    self.bus.publish({"type": "asset_empty", "asset": asset})

            results: Dict[str, dict] = {}
            for asset, df in per_asset.items():
                slot_stats = {}
                for t in sorted(pd.unique(df.index.time)):
                    hist = df[df.index.time == t]
                    counts = hist['color'].value_counts()
                    if counts.empty or counts.index[0] == 'DOJI':
                        continue
                    top = counts.index[0]
                    direction = 'CALL' if top == 'GREEN' else 'PUT'
                    total = int(counts.sum())
                    wins = int(counts[top])
                    acc = wins / total if total else 0
                    slot_stats[t.strftime('%H:%M')] = {
                        'direction': direction,
                        'accuracy': acc,
                        'total': total,
                    }
                results[asset] = {
                    'asset': asset,
                    'timeframe': self.timeframe,
                    'slots': slot_stats,
                }
                self.bus.publish({"type": "backtest_done", "asset": asset, "slots": len(slot_stats)})
            self.results = results
            self.bus.publish({"type": "catalog_done", "assets": list(results.keys())})
        except Exception as e:
            self.bus.publish({"type": "error", "message": str(e)})
        finally:
            with self._lock:
                self._running = False


def create_app(email: str, password: str, assets: List[str], timeframe: int) -> Flask:
    service = CatalogService(email, password, assets, timeframe)
    web_dir = Path(__file__).resolve().parent.parent / "web"
    static_dir = str(web_dir / "static")
    templates_dir = str(web_dir / "templates")
    app = Flask(__name__, static_folder=static_dir, template_folder=templates_dir)

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.post("/run")
    def run():
        day_str = request.json.get('date') if request.is_json else None
        signal_day = datetime.now() if not day_str else datetime.strptime(day_str, '%d/%m/%Y')
        lookback = int(request.args.get('lookback', 15))
        threading.Thread(target=service.run_catalog, args=(signal_day, lookback), daemon=True).start()
        return jsonify({"status": "started"})

    @app.get("/results")
    def results():
        return jsonify(service.results)

    @app.get("/events")
    def events():
        limit = int(request.args.get('limit', 100))
        return jsonify(service.bus.latest(limit))

    @app.get("/stream")
    def stream():
        q: queue.Queue = queue.Queue(maxsize=1000)

        def handler(evt):
            try:
                q.put_nowait(evt)
            except Exception:
                pass
        service.bus.subscribe(handler)

        def gen():
            try:
                yield "data: {}\n\n"
                while True:
                    evt = q.get()
                    yield f"data: {json.dumps(evt)}\n\n"
            except GeneratorExit:
                service.bus.unsubscribe(handler)
        headers = {
            "Content-Type": "text/event-stream",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
        return Response(stream_with_context(gen()), headers=headers)

    return app