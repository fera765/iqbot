import numpy as np
import pandas as pd
from typing import Dict, List, Optional

class TradingStrategy:
    """Classe base para estratégias de trading"""
    
    def __init__(self, config):
        self.config = config
        self.name = "Base Strategy"
    
    def calculate_signal(self, candles: List[Dict]) -> Optional[str]:
        """
        Calcula o sinal de trading
        Retorna: 'call', 'put' ou None
        """
        raise NotImplementedError
    
    def get_candles_dataframe(self, candles: List[Dict]) -> pd.DataFrame:
        """Converte lista de candles para DataFrame"""
        df = pd.DataFrame(candles)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df['close'] = df['close'].astype(float)
        df['open'] = df['open'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        df['volume'] = df['volume'].astype(float)
        return df

class RSIStrategy(TradingStrategy):
    """Estratégia baseada no RSI (Relative Strength Index)"""
    
    def __init__(self, config):
        super().__init__(config)
        self.name = "RSI Strategy"
        self.period = config.RSI_PERIOD
        self.overbought = config.RSI_OVERBOUGHT
        self.oversold = config.RSI_OVERSOLD
    
    def calculate_rsi(self, prices: List[float], period: int = 14) -> float:
        """Calcula o RSI"""
        if len(prices) < period + 1:
            return 50.0
        
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_signal(self, candles: List[Dict]) -> Optional[str]:
        if len(candles) < self.period + 1:
            return None
        
        df = self.get_candles_dataframe(candles)
        prices = df['close'].tolist()
        
        rsi = self.calculate_rsi(prices, self.period)
        
        # Sinal de compra quando RSI está oversold
        if rsi < self.oversold:
            return 'call'
        
        # Sinal de venda quando RSI está overbought
        elif rsi > self.overbought:
            return 'put'
        
        return None

class MACDStrategy(TradingStrategy):
    """Estratégia baseada no MACD (Moving Average Convergence Divergence)"""
    
    def __init__(self, config):
        super().__init__(config)
        self.name = "MACD Strategy"
        self.fast_period = 12
        self.slow_period = 26
        self.signal_period = 9
    
    def calculate_ema(self, prices: List[float], period: int) -> List[float]:
        """Calcula EMA (Exponential Moving Average)"""
        ema = []
        multiplier = 2 / (period + 1)
        
        for i, price in enumerate(prices):
            if i == 0:
                ema.append(price)
            else:
                ema.append((price * multiplier) + (ema[i-1] * (1 - multiplier)))
        
        return ema
    
    def calculate_signal(self, candles: List[Dict]) -> Optional[str]:
        if len(candles) < self.slow_period + self.signal_period:
            return None
        
        df = self.get_candles_dataframe(candles)
        prices = df['close'].tolist()
        
        # Calcula EMAs
        ema_fast = self.calculate_ema(prices, self.fast_period)
        ema_slow = self.calculate_ema(prices, self.slow_period)
        
        # Calcula MACD line
        macd_line = [fast - slow for fast, slow in zip(ema_fast, ema_slow)]
        
        # Calcula signal line
        signal_line = self.calculate_ema(macd_line, self.signal_period)
        
        if len(macd_line) < 2 or len(signal_line) < 2:
            return None
        
        # Sinal de compra quando MACD cruza acima da signal line
        if macd_line[-1] > signal_line[-1] and macd_line[-2] <= signal_line[-2]:
            return 'call'
        
        # Sinal de venda quando MACD cruza abaixo da signal line
        elif macd_line[-1] < signal_line[-1] and macd_line[-2] >= signal_line[-2]:
            return 'put'
        
        return None

class BollingerBandsStrategy(TradingStrategy):
    """Estratégia baseada nas Bandas de Bollinger"""
    
    def __init__(self, config):
        super().__init__(config)
        self.name = "Bollinger Bands Strategy"
        self.period = 20
        self.std_dev = 2
    
    def calculate_bollinger_bands(self, prices: List[float]) -> tuple:
        """Calcula as Bandas de Bollinger"""
        if len(prices) < self.period:
            return None, None, None
        
        sma = np.mean(prices[-self.period:])
        std = np.std(prices[-self.period:])
        
        upper_band = sma + (self.std_dev * std)
        lower_band = sma - (self.std_dev * std)
        
        return upper_band, sma, lower_band
    
    def calculate_signal(self, candles: List[Dict]) -> Optional[str]:
        if len(candles) < self.period:
            return None
        
        df = self.get_candles_dataframe(candles)
        prices = df['close'].tolist()
        current_price = prices[-1]
        
        upper, middle, lower = self.calculate_bollinger_bands(prices)
        
        if upper is None:
            return None
        
        # Sinal de compra quando preço toca a banda inferior
        if current_price <= lower:
            return 'call'
        
        # Sinal de venda quando preço toca a banda superior
        elif current_price >= upper:
            return 'put'
        
        return None

class RandomStrategy(TradingStrategy):
    """Estratégia aleatória para testes"""
    
    def __init__(self, config):
        super().__init__(config)
        self.name = "Random Strategy"
    
    def calculate_signal(self, candles: List[Dict]) -> Optional[str]:
        # 30% de chance de gerar um sinal
        if np.random.random() < 0.3:
            return np.random.choice(['call', 'put'])
        return None

def get_strategy(config) -> TradingStrategy:
    """Factory para criar estratégias"""
    strategies = {
        'RSI': RSIStrategy,
        'MACD': MACDStrategy,
        'BOLLINGER': BollingerBandsStrategy,
        'RANDOM': RandomStrategy
    }
    
    strategy_class = strategies.get(config.STRATEGY, RSIStrategy)
    return strategy_class(config)