from __future__ import annotations
from typing import List
from .base import Signal, BaseStrategy
from app.indicators import majority_color


class MHI3Strategy(BaseStrategy):
    name = "MHI-3"

    def generate_signal(self, candles: List[dict]) -> Signal:
        if len(candles) < 3:
            return Signal(None, "not_enough_candles")
        maj = majority_color(candles, 3)
        if maj is None:
            return Signal(None, "tie_majority")
        if maj == "green":
            return Signal("put", "mhi3_opposite_majority_green")
        else:
            return Signal("call", "mhi3_opposite_majority_red")


class MHI5Strategy(BaseStrategy):
    name = "MHI-5"

    def generate_signal(self, candles: List[dict]) -> Signal:
        if len(candles) < 5:
            return Signal(None, "not_enough_candles")
        maj = majority_color(candles, 5)
        if maj is None:
            return Signal(None, "tie_majority")
        if maj == "green":
            return Signal("put", "mhi5_opposite_majority_green")
        else:
            return Signal("call", "mhi5_opposite_majority_red")