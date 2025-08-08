from dataclasses import dataclass, field
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    IQ_EMAIL: str
    IQ_PASSWORD: str
    IQ_ACCOUNT_TYPE: str = "PRACTICE"

    ASSETS: List[str] = field(default_factory=lambda: ["EURUSD"])
    STAKE: float = 2.0
    TIMEFRAME_SECONDS: int = 60
    MAX_GALES: int = 2
    MARTINGALE_MULTIPLIER: float = 2.1

    BACKTEST_CANDLES: int = 1500
    MIN_ACCURACY_TO_SELECT: float = 0.9

    CONFLUENCE_THRESHOLD: int = 60

    HOST: str = "127.0.0.1"
    PORT: int = 8000

    @classmethod
    def from_env(cls) -> "Settings":
        env = os.getenv
        assets_raw = env("ASSETS", "EURUSD")
        assets = [a.strip().upper() for a in assets_raw.split(",") if a.strip()]
        return cls(
            IQ_EMAIL=env("IQ_EMAIL", ""),
            IQ_PASSWORD=env("IQ_PASSWORD", ""),
            IQ_ACCOUNT_TYPE=env("IQ_ACCOUNT_TYPE", "PRACTICE"),
            ASSETS=assets,
            STAKE=float(env("STAKE", "2")),
            TIMEFRAME_SECONDS=int(env("TIMEFRAME_SECONDS", "60")),
            MAX_GALES=int(env("MAX_GALES", "2")),
            MARTINGALE_MULTIPLIER=float(env("MARTINGALE_MULTIPLIER", "2.1")),
            BACKTEST_CANDLES=int(env("BACKTEST_CANDLES", "1500")),
            MIN_ACCURACY_TO_SELECT=float(env("MIN_ACCURACY_TO_SELECT", "0.9")),
            CONFLUENCE_THRESHOLD=int(env("CONFLUENCE_THRESHOLD", "60")),
            HOST=env("HOST", "127.0.0.1"),
            PORT=int(env("PORT", "8000")),
        )