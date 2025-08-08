from __future__ import annotations
from typing import Dict, List
from .backtester import Backtester


def build_catalog(assets: List[str], timeframe_seconds: int, candles_by_asset: Dict[str, List[dict]], backtester: Backtester) -> Dict[str, List[dict]]:
    catalog: Dict[str, List[dict]] = {}
    for asset in assets:
        candles = candles_by_asset.get(asset, [])
        if not candles:
            continue
        results = backtester.backtest_on_candles(candles)
        serializable = []
        for m in results:
            serializable.append({
                "asset": asset,
                "timeframe_seconds": timeframe_seconds,
                "strategy_name": m.strategy_name,
                "total_signals": m.total_signals,
                "taken_trades": m.taken_trades,
                "wins": m.wins,
                "losses": m.losses,
                "equals": m.equals,
                "accuracy": m.accuracy,
            })
        catalog[asset] = serializable
    return catalog