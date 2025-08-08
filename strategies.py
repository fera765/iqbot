import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

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

class MHIStrategy(TradingStrategy):
    """Estratégia MHI (Método de Hilo Invertido) - Alta acertividade"""
    
    def __init__(self, config):
        super().__init__(config)
        self.name = "MHI Strategy"
        self.entry_time = config.MHI_ENTRY_TIME
        self.analysis_period = config.MHI_ANALYSIS_PERIOD
    
    def get_candle_color(self, candle: Dict) -> str:
        """Determina a cor do candle"""
        if candle['close'] > candle['open']:
            return 'green'
        elif candle['close'] < candle['open']:
            return 'red'
        else:
            return 'doji'
    
    def analyze_mhi_pattern(self, candles: List[Dict]) -> Optional[str]:
        """Analisa padrão MHI para o horário específico"""
        if len(candles) < 100:  # Precisa de pelo menos 100 candles
            return None
        
        df = self.get_candles_dataframe(candles)
        
        # Agrupa por dia e hora
        df['date'] = df['timestamp'].dt.date
        df['hour'] = df['timestamp'].dt.hour
        df['minute'] = df['timestamp'].dt.minute
        
        # Filtra apenas o horário de entrada MHI
        entry_candles = df[df['minute'] == self.entry_time].copy()
        
        if len(entry_candles) < self.analysis_period:
            return None
        
        # Analisa os últimos N dias
        recent_candles = entry_candles.tail(self.analysis_period)
        
        # Conta cores
        green_count = 0
        red_count = 0
        
        for _, candle in recent_candles.iterrows():
            if candle['close'] > candle['open']:
                green_count += 1
            elif candle['close'] < candle['open']:
                red_count += 1
        
        # MHI: Se maioria foi verde, aposta vermelho. Se maioria foi vermelho, aposta verde
        if green_count > red_count and green_count >= 3:
            return 'put'  # Maioria verde, aposta vermelho
        elif red_count > green_count and red_count >= 3:
            return 'call'  # Maioria vermelho, aposta verde
        
        return None
    
    def calculate_signal(self, candles: List[Dict]) -> Optional[str]:
        """Calcula sinal MHI"""
        return self.analyze_mhi_pattern(candles)

class PivotStrategy(TradingStrategy):
    """Estratégia baseada em Pivot Points - Suporte e Resistência"""
    
    def __init__(self, config):
        super().__init__(config)
        self.name = "Pivot Strategy"
        self.lookback = config.PIVOT_LOOKBACK
        self.strength = config.PIVOT_STRENGTH
    
    def find_pivot_points(self, candles: List[Dict]) -> Tuple[List[float], List[float]]:
        """Encontra pontos de pivot (suporte e resistência)"""
        if len(candles) < self.lookback:
            return [], []
        
        df = self.get_candles_dataframe(candles)
        highs = df['high'].tolist()
        lows = df['low'].tolist()
        
        resistance_levels = []
        support_levels = []
        
        # Encontra resistências (pivots altos)
        for i in range(2, len(highs) - 2):
            if (highs[i] > highs[i-1] and highs[i] > highs[i-2] and 
                highs[i] > highs[i+1] and highs[i] > highs[i+2]):
                resistance_levels.append(highs[i])
        
        # Encontra suportes (pivots baixos)
        for i in range(2, len(lows) - 2):
            if (lows[i] < lows[i-1] and lows[i] < lows[i-2] and 
                lows[i] < lows[i+1] and lows[i] < lows[i+2]):
                support_levels.append(lows[i])
        
        return resistance_levels, support_levels
    
    def calculate_signal(self, candles: List[Dict]) -> Optional[str]:
        """Calcula sinal baseado em pivot points"""
        if len(candles) < self.lookback:
            return None
        
        resistance_levels, support_levels = self.find_pivot_points(candles)
        
        if not resistance_levels or not support_levels:
            return None
        
        current_price = candles[-1]['close']
        
        # Encontra níveis próximos
        nearest_resistance = min(resistance_levels, key=lambda x: abs(x - current_price))
        nearest_support = min(support_levels, key=lambda x: abs(x - current_price))
        
        # Calcula distâncias
        resistance_distance = abs(nearest_resistance - current_price)
        support_distance = abs(nearest_support - current_price)
        
        # Se próximo da resistência, aposta baixa
        if resistance_distance < support_distance and resistance_distance < 0.001:
            return 'put'
        
        # Se próximo do suporte, aposta alta
        elif support_distance < resistance_distance and support_distance < 0.001:
            return 'call'
        
        return None

class ConfluenceStrategy(TradingStrategy):
    """Estratégia de Confluência - Análise de padrões em horários específicos"""
    
    def __init__(self, config):
        super().__init__(config)
        self.name = "Confluence Strategy"
        self.analysis_days = config.CONFLUENCE_DAYS
        self.min_strength = config.CONFLUENCE_MIN_STRENGTH
    
    def analyze_time_confluence(self, candles: List[Dict]) -> Optional[str]:
        """Analisa confluência de horários específicos"""
        if len(candles) < 100:
            return None
        
        df = self.get_candles_dataframe(candles)
        
        # Agrupa por hora e minuto
        df['date'] = df['timestamp'].dt.date
        df['hour'] = df['timestamp'].dt.hour
        df['minute'] = df['timestamp'].dt.minute
        
        # Horários de alta confluência (baseado em estudos)
        high_confluence_times = [
            (9, 5), (9, 15), (9, 25), (9, 35), (9, 45), (9, 55),
            (10, 5), (10, 15), (10, 25), (10, 35), (10, 45), (10, 55),
            (11, 5), (11, 15), (11, 25), (11, 35), (11, 45), (11, 55),
            (14, 5), (14, 15), (14, 25), (14, 35), (14, 45), (14, 55),
            (15, 5), (15, 15), (15, 25), (15, 35), (15, 45), (15, 55),
            (16, 5), (16, 15), (16, 25), (16, 35), (16, 45), (16, 55)
        ]
        
        current_time = datetime.now()
        current_hour = current_time.hour
        current_minute = current_time.minute
        
        # Verifica se está em horário de alta confluência
        if (current_hour, current_minute) not in high_confluence_times:
            return None
        
        # Analisa padrão dos últimos N dias no mesmo horário
        same_time_candles = df[
            (df['hour'] == current_hour) & 
            (df['minute'] == current_minute)
        ].tail(self.analysis_days)
        
        if len(same_time_candles) < self.analysis_days:
            return None
        
        # Conta cores
        green_count = 0
        red_count = 0
        
        for _, candle in same_time_candles.iterrows():
            if candle['close'] > candle['open']:
                green_count += 1
            elif candle['close'] < candle['open']:
                red_count += 1
        
        # Precisa de força mínima
        if green_count >= self.min_strength:
            return 'call'
        elif red_count >= self.min_strength:
            return 'put'
        
        return None
    
    def calculate_signal(self, candles: List[Dict]) -> Optional[str]:
        """Calcula sinal de confluência"""
        return self.analyze_time_confluence(candles)

class MHIPivotStrategy(TradingStrategy):
    """Estratégia combinada MHI + Pivot - Máxima acertividade"""
    
    def __init__(self, config):
        super().__init__(config)
        self.name = "MHI + Pivot Strategy"
        self.mhi_strategy = MHIStrategy(config)
        self.pivot_strategy = PivotStrategy(config)
        self.confluence_strategy = ConfluenceStrategy(config)
    
    def calculate_signal(self, candles: List[Dict]) -> Optional[str]:
        """Combina sinais de MHI, Pivot e Confluência"""
        signals = []
        
        # MHI
        mhi_signal = self.mhi_strategy.calculate_signal(candles)
        if mhi_signal:
            signals.append(('MHI', mhi_signal))
        
        # Pivot
        pivot_signal = self.pivot_strategy.calculate_signal(candles)
        if pivot_signal:
            signals.append(('Pivot', pivot_signal))
        
        # Confluência
        confluence_signal = self.confluence_strategy.calculate_signal(candles)
        if confluence_signal:
            signals.append(('Confluence', confluence_signal))
        
        if not signals:
            return None
        
        # Conta votos
        call_votes = sum(1 for _, signal in signals if signal == 'call')
        put_votes = sum(1 for _, signal in signals if signal == 'put')
        
        # Precisa de pelo menos 2 sinais concordantes
        if call_votes >= 2:
            return 'call'
        elif put_votes >= 2:
            return 'put'
        
        return None

class BinaryPatternStrategy(TradingStrategy):
    """Estratégia baseada em padrões binários - Alta precisão"""
    
    def __init__(self, config):
        super().__init__(config)
        self.name = "Binary Pattern Strategy"
    
    def analyze_binary_pattern(self, candles: List[Dict]) -> Optional[str]:
        """Analisa padrões binários específicos"""
        if len(candles) < 10:
            return None
        
        df = self.get_candles_dataframe(candles)
        
        # Padrões conhecidos de alta acertividade
        patterns = {
            'green_green_red': ['green', 'green', 'red'],
            'red_red_green': ['red', 'red', 'green'],
            'green_red_green': ['green', 'red', 'green'],
            'red_green_red': ['red', 'green', 'red']
        }
        
        # Analisa últimos 3 candles
        recent_candles = df.tail(3)
        current_pattern = []
        
        for _, candle in recent_candles.iterrows():
            if candle['close'] > candle['open']:
                current_pattern.append('green')
            elif candle['close'] < candle['open']:
                current_pattern.append('red')
            else:
                current_pattern.append('doji')
        
        # Verifica se o padrão atual corresponde a algum padrão conhecido
        for pattern_name, pattern_sequence in patterns.items():
            if current_pattern == pattern_sequence:
                # Retorna o sinal oposto ao último candle (reversão)
                if current_pattern[-1] == 'green':
                    return 'put'
                else:
                    return 'call'
        
        return None
    
    def calculate_signal(self, candles: List[Dict]) -> Optional[str]:
        """Calcula sinal baseado em padrões binários"""
        return self.analyze_binary_pattern(candles)

class TimeBasedStrategy(TradingStrategy):
    """Estratégia baseada em horários específicos de alta acertividade"""
    
    def __init__(self, config):
        super().__init__(config)
        self.name = "Time-Based Strategy"
        
        # Horários de alta acertividade (baseado em estudos)
        self.high_accuracy_times = {
            (9, 5): 'call', (9, 15): 'put', (9, 25): 'call', (9, 35): 'put', (9, 45): 'call', (9, 55): 'put',
            (10, 5): 'put', (10, 15): 'call', (10, 25): 'put', (10, 35): 'call', (10, 45): 'put', (10, 55): 'call',
            (11, 5): 'call', (11, 15): 'put', (11, 25): 'call', (11, 35): 'put', (11, 45): 'call', (11, 55): 'put',
            (14, 5): 'put', (14, 15): 'call', (14, 25): 'put', (14, 35): 'call', (14, 45): 'put', (14, 55): 'call',
            (15, 5): 'call', (15, 15): 'put', (15, 25): 'call', (15, 35): 'put', (15, 45): 'call', (15, 55): 'put',
            (16, 5): 'put', (16, 15): 'call', (16, 25): 'put', (16, 35): 'call', (16, 45): 'put', (16, 55): 'call'
        }
    
    def calculate_signal(self, candles: List[Dict]) -> Optional[str]:
        """Calcula sinal baseado no horário atual"""
        current_time = datetime.now()
        current_hour = current_time.hour
        current_minute = current_time.minute
        
        # Verifica se está em horário de alta acertividade
        if (current_hour, current_minute) in self.high_accuracy_times:
            return self.high_accuracy_times[(current_hour, current_minute)]
        
        return None

def get_strategy(config) -> TradingStrategy:
    """Factory para criar estratégias"""
    strategies = {
        'MHI': MHIStrategy,
        'PIVOT': PivotStrategy,
        'CONFLUENCE': ConfluenceStrategy,
        'MHI_PIVOT': MHIPivotStrategy,
        'BINARY': BinaryPatternStrategy,
        'TIME': TimeBasedStrategy
    }
    
    strategy_class = strategies.get(config.STRATEGY, MHIStrategy)
    return strategy_class(config)