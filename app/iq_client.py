from __future__ import annotations
from typing import List, Tuple, Optional
from iqoptionapi.stable_api import IQ_Option
import time
import threading


class IQClient:
    def __init__(self, email: str, password: str, account_type: str = "PRACTICE") -> None:
        self.email = email
        self.password = password
        self.account_type = account_type
        self._api: Optional[IQ_Option] = None
        self._lock = threading.Lock()

    def connect(self) -> None:
        with self._lock:
            if self._api is None:
                self._api = IQ_Option(self.email, self.password)
            else:
                try:
                    self._api.disconnect()
                except Exception:
                    pass
                self._api = IQ_Option(self.email, self.password)
            self._api.connect()
            self._api.change_balance(self.account_type)

    def ensure_connected(self) -> None:
        if self._api is None:
            self.connect()
        else:
            if not self._api.check_connect():  # type: ignore
                self.connect()

    def get_server_time(self) -> int:
        self.ensure_connected()
        return int(time.time())

    def get_candles(self, asset: str, timeframe_seconds: int, count: int, endtime: Optional[int] = None) -> List[dict]:
        self.ensure_connected()
        if endtime is None:
            endtime = int(time.time())
        candles = self._api.get_candles(asset, timeframe_seconds, count, endtime)  # type: ignore
        # Ensure candles are sorted by time
        candles_sorted = sorted(candles, key=lambda c: c["from"])  # type: ignore
        return candles_sorted

    def buy(self, amount: float, asset: str, direction: str, duration_minutes: int = 1) -> Tuple[bool, Optional[int]]:
        self.ensure_connected()
        ok, order_id = self._api.buy(amount, asset, direction, duration_minutes)  # type: ignore
        return ok, order_id

    def check_win_v4(self, order_id: int) -> Tuple[str, float]:
        self.ensure_connected()
        status, profit = self._api.check_win_v4(order_id)  # type: ignore
        return status, float(profit)