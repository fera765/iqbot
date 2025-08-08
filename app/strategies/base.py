from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Protocol


@dataclass
class Signal:
    action: Optional[str]  # "call" | "put" | None
    reason: str


@dataclass
class BacktestMetrics:
    asset: str
    timeframe_seconds: int
    strategy_name: str
    total_signals: int
    taken_trades: int
    wins: int
    losses: int
    equals: int
    accuracy: float


class Strategy(Protocol):
    name: str

    def generate_signal(self, candles: List[dict]) -> Signal:
        ...

    def backtest(
        self,
        candles: List[dict],
        confluence_fn,
        confluence_threshold: int,
    ) -> BacktestMetrics:
        total_signals = 0
        taken_trades = 0
        wins = 0
        losses = 0
        equals = 0

        # We simulate by looking at the next candle direction
        # A trade is taken only if confluence >= threshold
        for i in range(20, len(candles) - 1):  # leave enough warmup for indicators
            window = candles[: i + 1]
            signal = self.generate_signal(window)
            if signal.action is None:
                continue
            total_signals += 1
            score = confluence_fn(window, signal.action)
            if score < confluence_threshold:
                continue
            taken_trades += 1
            this_candle = candles[i]
            next_candle = candles[i + 1]
            this_close = this_candle["close"]
            next_close = next_candle["close"]
            next_open = next_candle["open"]
            # Determine next candle direction
            if next_close > next_open:
                next_dir = "call"
            elif next_close < next_open:
                next_dir = "put"
            else:
                next_dir = "equal"
            if next_dir == "equal":
                equals += 1
            elif next_dir == signal.action:
                wins += 1
            else:
                losses += 1

        accuracy = (wins / taken_trades) if taken_trades > 0 else 0.0
        return BacktestMetrics(
            asset="",
            timeframe_seconds=0,
            strategy_name=self.name,
            total_signals=total_signals,
            taken_trades=taken_trades,
            wins=wins,
            losses=losses,
            equals=equals,
            accuracy=accuracy,
        )