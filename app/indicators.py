from __future__ import annotations
from typing import List, Tuple
import numpy as np


def compute_ema(values: List[float], period: int) -> List[float]:
    if len(values) < period:
        return [np.nan] * len(values)
    ema = []
    k = 2 / (period + 1)
    ema_value = float(np.mean(values[:period]))
    ema.extend([np.nan] * (period - 1))
    ema.append(ema_value)
    for price in values[period:]:
        ema_value = price * k + ema_value * (1 - k)
        ema.append(ema_value)
    return ema


def compute_rsi(values: List[float], period: int = 14) -> List[float]:
    if len(values) <= period:
        return [np.nan] * len(values)
    deltas = np.diff(values)
    gains = np.where(deltas > 0, deltas, 0.0)
    losses = np.where(deltas < 0, -deltas, 0.0)
    avg_gain = np.zeros_like(values, dtype=float)
    avg_loss = np.zeros_like(values, dtype=float)
    avg_gain[period] = np.mean(gains[:period])
    avg_loss[period] = np.mean(losses[:period])
    for i in range(period + 1, len(values)):
        avg_gain[i] = (avg_gain[i - 1] * (period - 1) + gains[i - 1]) / period
        avg_loss[i] = (avg_loss[i - 1] * (period - 1) + losses[i - 1]) / period
    rs = np.divide(avg_gain, avg_loss, out=np.zeros_like(avg_gain), where=avg_loss != 0)
    rsi = 100 - (100 / (1 + rs))
    rsi[: period] = np.nan
    return rsi.tolist()


def compute_bollinger(values: List[float], period: int = 20, std_dev: float = 2.0) -> Tuple[List[float], List[float], List[float]]:
    if len(values) < period:
        nan_list = [np.nan] * len(values)
        return nan_list, nan_list, nan_list
    ma = []
    upper = []
    lower = []
    for i in range(len(values)):
        if i + 1 < period:
            ma.append(np.nan)
            upper.append(np.nan)
            lower.append(np.nan)
        else:
            window = values[i + 1 - period : i + 1]
            mean = float(np.mean(window))
            std = float(np.std(window))
            ma.append(mean)
            upper.append(mean + std_dev * std)
            lower.append(mean - std_dev * std)
    return ma, upper, lower


def candle_color(open_price: float, close_price: float) -> str:
    if close_price > open_price:
        return "green"
    if close_price < open_price:
        return "red"
    return "doji"


def majority_color(candles: List[dict], lookback: int) -> str | None:
    recent = candles[-lookback:]
    greens = reds = 0
    for c in recent:
        color = candle_color(c["open"], c["close"])  # type: ignore
        if color == "green":
            greens += 1
        elif color == "red":
            reds += 1
    if greens == reds:
        return None
    return "green" if greens > reds else "red"