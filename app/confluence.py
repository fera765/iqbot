from __future__ import annotations
from typing import List
from .indicators import compute_ema, compute_rsi, compute_bollinger


class ConfluenceEngine:
    def __init__(self, rsi_period: int = 14, ema_period: int = 20, bb_period: int = 20, bb_std: float = 2.0) -> None:
        self.rsi_period = rsi_period
        self.ema_period = ema_period
        self.bb_period = bb_period
        self.bb_std = bb_std

    def score(self, candles: List[dict], action: str) -> int:
        closes = [c["close"] for c in candles]
        opens = [c["open"] for c in candles]
        ema = compute_ema(closes, self.ema_period)
        rsi = compute_rsi(closes, self.rsi_period)
        ma, upper, lower = compute_bollinger(closes, self.bb_period, self.bb_std)

        idx = len(closes) - 1
        if idx < 1:
            return 0

        score = 0
        max_score = 100
        # EMA slope + price position
        if idx >= 2 and not (ema[idx] != ema[idx]):  # check not NaN
            ema_slope = ema[idx] - ema[idx - 1]
            price_above_ema = closes[idx] > ema[idx]
            if action == "call":
                if ema_slope > 0:
                    score += 20
                if price_above_ema:
                    score += 10
            if action == "put":
                if ema_slope < 0:
                    score += 20
                if not price_above_ema:
                    score += 10

        # RSI extreme alignment
        rsi_val = rsi[idx]
        if rsi_val == rsi_val:  # not NaN
            if action == "call" and rsi_val <= 35:
                score += 25
            if action == "put" and rsi_val >= 65:
                score += 25

        # Bollinger proximity
        up = upper[idx]
        lo = lower[idx]
        if up == up and lo == lo:  # not NaN
            if action == "call" and closes[idx] <= lo:
                score += 20
            if action == "put" and closes[idx] >= up:
                score += 20

        # Candle momentum confirmation
        prev_close = closes[idx - 1]
        prev_open = opens[idx - 1]
        if action == "call" and prev_close < prev_open:
            score += 5  # previous candle red (potential exhaustion)
        if action == "put" and prev_close > prev_open:
            score += 5  # previous candle green

        # Clamp
        score = max(0, min(score, max_score))
        return int(score)