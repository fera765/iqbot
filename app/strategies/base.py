from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Protocol


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


class BaseStrategy:
    name: str = "Base"

    def generate_signal(self, candles: List[dict]) -> Signal:  # pragma: no cover
        return Signal(None, "not_implemented")

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

        for i in range(20, len(candles) - 1):
            window = candles[: i + 1]
            signal = self.generate_signal(window)
            if signal.action is None:
                continue
            total_signals += 1
            score = confluence_fn(window, signal.action)
            if score < confluence_threshold:
                continue
            taken_trades += 1
            next_candle = candles[i + 1]
            next_close = next_candle["close"]
            next_open = next_candle["open"]
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