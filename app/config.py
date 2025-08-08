from pydantic import BaseModel, Field, field_validator
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseModel):
    IQ_EMAIL: str = Field(..., description="IQ Option email")
    IQ_PASSWORD: str = Field(..., description="IQ Option password")
    IQ_ACCOUNT_TYPE: str = Field("PRACTICE", description="PRACTICE or REAL")

    ASSETS: List[str] = Field(default_factory=lambda: ["EURUSD"], description="Comma-separated list of assets")
    STAKE: float = Field(2.0, description="Stake amount per entry")
    TIMEFRAME_SECONDS: int = Field(60, description="Candle timeframe in seconds")
    MAX_GALES: int = Field(2, description="Max martingale steps")
    MARTINGALE_MULTIPLIER: float = Field(2.1, description="Multiplier for martingale stake")

    BACKTEST_CANDLES: int = Field(1500, description="Number of candles for backtesting")
    MIN_ACCURACY_TO_SELECT: float = Field(0.9, description="Minimum accuracy threshold to select primary strategy")

    CONFLUENCE_THRESHOLD: int = Field(60, description="Confluence score threshold (0-100)")

    HOST: str = Field("127.0.0.1", description="Web server host")
    PORT: int = Field(8000, description="Web server port")

    class Config:
        arbitrary_types_allowed = True

    @field_validator("ASSETS", mode="before")
    @classmethod
    def parse_assets(cls, v):
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            return [asset.strip().upper() for asset in v.split(",") if asset.strip()]
        return ["EURUSD"]

    @classmethod
    def from_env(cls) -> "Settings":
        data = {k: os.getenv(k) for k in cls.model_fields.keys()}
        # Convert types where needed
        if data.get("STAKE") is not None:
            data["STAKE"] = float(data["STAKE"])  # type: ignore
        if data.get("TIMEFRAME_SECONDS") is not None:
            data["TIMEFRAME_SECONDS"] = int(data["TIMEFRAME_SECONDS"])  # type: ignore
        if data.get("MAX_GALES") is not None:
            data["MAX_GALES"] = int(data["MAX_GALES"])  # type: ignore
        if data.get("MARTINGALE_MULTIPLIER") is not None:
            data["MARTINGALE_MULTIPLIER"] = float(data["MARTINGALE_MULTIPLIER"])  # type: ignore
        if data.get("BACKTEST_CANDLES") is not None:
            data["BACKTEST_CANDLES"] = int(data["BACKTEST_CANDLES"])  # type: ignore
        if data.get("MIN_ACCURACY_TO_SELECT") is not None:
            data["MIN_ACCURACY_TO_SELECT"] = float(data["MIN_ACCURACY_TO_SELECT"])  # type: ignore
        if data.get("CONFLUENCE_THRESHOLD") is not None:
            data["CONFLUENCE_THRESHOLD"] = int(data["CONFLUENCE_THRESHOLD"])  # type: ignore
        if data.get("PORT") is not None:
            data["PORT"] = int(data["PORT"])  # type: ignore
        return cls(**data)  # type: ignore