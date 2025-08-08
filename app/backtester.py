from __future__ import annotations
from typing import List, Tuple, Dict
from .strategies.mhi import MHI3Strategy, MHI5Strategy
from .strategies.base import Strategy, BacktestMetrics
from .confluence import ConfluenceEngine


class Backtester:
    def __init__(self, confluence_threshold: int) -> None:
        self.confluence = ConfluenceEngine()
        self.confluence_threshold = confluence_threshold
        self.strategies: List[Strategy] = [MHI3Strategy(), MHI5Strategy()]

    def backtest_on_candles(self, candles: List[dict]) -> List[BacktestMetrics]:
        results: List[BacktestMetrics] = []
        for strat in self.strategies:
            m = strat.backtest(candles, self.confluence.score, self.confluence_threshold)
            results.append(m)
        return results

    def pick_best(self, asset: str, timeframe_seconds: int, candles: List[dict]) -> Tuple[Strategy, BacktestMetrics]:
        best_strat = None
        best_metrics = None
        for strat in self.strategies:
            m = strat.backtest(candles, self.confluence.score, self.confluence_threshold)
            m.asset = asset
            m.timeframe_seconds = timeframe_seconds
            if best_metrics is None or m.accuracy > best_metrics.accuracy:
                best_metrics = m
                best_strat = strat
        assert best_strat is not None and best_metrics is not None
        return best_strat, best_metrics