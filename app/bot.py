from __future__ import annotations
import threading
import time
from typing import List, Optional, Dict, Any, Tuple
from .iq_client import IQClient
from .config import Settings
from .backtester import Backtester
from .confluence import ConfluenceEngine
from .strategies.base import Strategy, BacktestMetrics, Signal


class EventBus:
    def __init__(self) -> None:
        self._subscribers: List = []
        self._lock = threading.Lock()

    def subscribe(self, handler) -> None:
        with self._lock:
            self._subscribers.append(handler)

    def unsubscribe(self, handler) -> None:
        with self._lock:
            self._subscribers = [h for h in self._subscribers if h != handler]

    def publish(self, event: Dict[str, Any]) -> None:
        with self._lock:
            subscribers = list(self._subscribers)
        for h in subscribers:
            try:
                h(event)
            except Exception:
                pass


class TradingBot(threading.Thread):
    def __init__(self, settings: Settings, event_bus: EventBus) -> None:
        super().__init__(daemon=True)
        self.settings = settings
        self.event_bus = event_bus
        self.client = IQClient(settings.IQ_EMAIL, settings.IQ_PASSWORD, settings.IQ_ACCOUNT_TYPE)
        self.confluence = ConfluenceEngine()
        self.backtester = Backtester(confluence_threshold=settings.CONFLUENCE_THRESHOLD)
        self._stop = threading.Event()
        self.current_strategy: Optional[Strategy] = None
        self.current_metrics: Optional[BacktestMetrics] = None
        self.current_asset: Optional[str] = None
        self.pnl: float = 0.0

    def stop(self):
        self._stop.set()

    def _publish(self, type_: str, **kwargs):
        event = {"type": type_, **kwargs, "ts": int(time.time())}
        self.event_bus.publish(event)

    def _sync_to_candle_close(self, timeframe_seconds: int):
        now = int(time.time())
        sleep_time = timeframe_seconds - (now % timeframe_seconds)
        time.sleep(sleep_time + 0.2)  # small buffer after close

    def _rebalance_strategy(self):
        # Fetch candles and pick best strategy for each asset; choose the overall best
        best: Optional[Tuple[str, Strategy, BacktestMetrics]] = None
        for asset in self.settings.ASSETS:
            candles = self.client.get_candles(asset, self.settings.TIMEFRAME_SECONDS, self.settings.BACKTEST_CANDLES)
            strat, metrics = self.backtester.pick_best(asset, self.settings.TIMEFRAME_SECONDS, candles)
            if best is None or metrics.accuracy > best[2].accuracy:
                best = (asset, strat, metrics)
        if best is not None:
            self.current_asset, self.current_strategy, self.current_metrics = best
            self._publish(
                "strategy_selected",
                asset=self.current_asset,
                strategy=self.current_strategy.name,
                accuracy=round(self.current_metrics.accuracy * 100, 2),
                taken_trades=self.current_metrics.taken_trades,
            )

    def run(self):
        self.client.ensure_connected()
        self._publish("bot_status", status="connected", account_type=self.settings.IQ_ACCOUNT_TYPE)
        self._rebalance_strategy()

        last_rebalance = time.time()
        while not self._stop.is_set():
            # Rebalance strategy every ~30 minutes or if accuracy below threshold and a better one emerges
            if time.time() - last_rebalance > 30 * 60 or self.current_strategy is None:
                try:
                    self._rebalance_strategy()
                except Exception as e:
                    self._publish("error", message=f"rebalance_failed: {e}")
                last_rebalance = time.time()

            if self.current_strategy is None or self.current_asset is None:
                time.sleep(5)
                continue

            # Wait close of current candle
            self._sync_to_candle_close(self.settings.TIMEFRAME_SECONDS)

            # Fetch fresh candles
            candles = self.client.get_candles(self.current_asset, self.settings.TIMEFRAME_SECONDS, 200)
            signal: Signal = self.current_strategy.generate_signal(candles)
            if signal.action is None:
                self._publish("no_trade", reason=signal.reason)
                continue

            score = self.confluence.score(candles, signal.action)
            if score < self.settings.CONFLUENCE_THRESHOLD:
                self._publish("filtered", reason="low_confluence", confluence=score)
                continue

            # Place trade
            direction = signal.action
            stake = self.settings.STAKE
            duration_minutes = self.settings.TIMEFRAME_SECONDS // 60
            if duration_minutes <= 0:
                duration_minutes = 1

            ok, order_id = self.client.buy(stake, self.current_asset, direction, duration_minutes)
            if not ok or order_id is None:
                self._publish("order_rejected", stake=stake, direction=direction)
                continue

            self._publish(
                "order_placed",
                order_id=order_id,
                asset=self.current_asset,
                direction=direction,
                stake=stake,
                strategy=self.current_strategy.name,
                confluence=score,
            )

            # Wait result
            time.sleep(self.settings.TIMEFRAME_SECONDS + 1)
            status, profit = self.client.check_win_v4(order_id)
            if status == "win":
                self.pnl += profit
                self._publish("order_result", order_id=order_id, result="win", profit=profit, pnl=self.pnl)
                continue
            elif status == "equal":
                self._publish("order_result", order_id=order_id, result="equal", profit=0.0, pnl=self.pnl)
                continue
            else:
                self.pnl -= stake
                self._publish("order_result", order_id=order_id, result="loss", profit=-stake, pnl=self.pnl)

            # Martingale steps
            last_result = status
            last_direction = direction
            for gale in range(1, self.settings.MAX_GALES + 1):
                new_stake = round(stake * (self.settings.MARTINGALE_MULTIPLIER ** gale), 2)
                # Enter immediately at next candle close
                self._sync_to_candle_close(self.settings.TIMEFRAME_SECONDS)
                candles = self.client.get_candles(self.current_asset, self.settings.TIMEFRAME_SECONDS, 200)
                # Optional: Keep same direction for martingale
                ok2, order_id2 = self.client.buy(new_stake, self.current_asset, last_direction, duration_minutes)
                if not ok2 or order_id2 is None:
                    self._publish("order_rejected", stake=new_stake, direction=last_direction, gale=gale)
                    break
                self._publish("order_placed", order_id=order_id2, asset=self.current_asset, direction=last_direction, stake=new_stake, strategy=f"{self.current_strategy.name}-GALE{gale}")
                time.sleep(self.settings.TIMEFRAME_SECONDS + 1)
                status2, profit2 = self.client.check_win_v4(order_id2)
                if status2 == "win":
                    self.pnl += profit2
                    self._publish("order_result", order_id=order_id2, result="win", profit=profit2, pnl=self.pnl, gale=gale)
                    break
                elif status2 == "equal":
                    self._publish("order_result", order_id=order_id2, result="equal", profit=0.0, pnl=self.pnl, gale=gale)
                    break
                else:
                    self.pnl -= new_stake
                    self._publish("order_result", order_id=order_id2, result="loss", profit=-new_stake, pnl=self.pnl, gale=gale)
                    # Continue gales until max reached

            # Check periodically if a better strategy appears > threshold
            try:
                asset = self.current_asset
                candles = self.client.get_candles(asset, self.settings.TIMEFRAME_SECONDS, self.settings.BACKTEST_CANDLES)
                best_strat, best_metrics = self.backtester.pick_best(asset, self.settings.TIMEFRAME_SECONDS, candles)
                if best_metrics.accuracy >= self.settings.MIN_ACCURACY_TO_SELECT and (
                    self.current_metrics is None or best_metrics.accuracy > self.current_metrics.accuracy
                ):
                    self.current_strategy = best_strat
                    self.current_metrics = best_metrics
                    self._publish("strategy_switched", asset=asset, strategy=best_strat.name, accuracy=round(best_metrics.accuracy * 100, 2))
            except Exception as e:
                self._publish("error", message=f"post_trade_rebalance_error: {e}")