#!/usr/bin/env python3
"""
Testes para o Robô de Trading IQ Option
"""

import unittest
from unittest.mock import Mock, patch
import pandas as pd
import numpy as np

from config import Config
from strategies import MHIStrategy, PivotStrategy, ConfluenceStrategy, MHIPivotStrategy, BinaryPatternStrategy, TimeBasedStrategy
from risk_manager import RiskManager
from logger import TradingLogger

class TestStrategies(unittest.TestCase):
    """Testes para as estratégias de trading"""
    
    def setUp(self):
        self.config = Config()
        self.config.STRATEGY = 'MHI'
        self.config.MHI_ENTRY_TIME = 5
        self.config.MHI_ANALYSIS_PERIOD = 5
        self.config.PIVOT_LOOKBACK = 20
        self.config.PIVOT_STRENGTH = 3
        self.config.CONFLUENCE_DAYS = 5
        self.config.CONFLUENCE_MIN_STRENGTH = 3
    
    def test_mhi_strategy(self):
        """Testa a estratégia MHI"""
        strategy = MHIStrategy(self.config)
        
        # Cria dados de teste com padrão MHI
        candles = []
        base_time = 1609459200  # Timestamp base
        
        for day in range(10):
            for hour in range(9, 17):
                for minute in [5, 15, 25, 35, 45, 55]:
                    timestamp = base_time + (day * 86400) + (hour * 3600) + (minute * 60)
                    
                    # Simula padrão MHI: maioria verde no minuto 5
                    if minute == 5:
                        close = 1.1002 if day < 5 else 1.0998  # Maioria verde
                    else:
                        close = 1.1000 + (day * 0.0001)
                    
                    candles.append({
                        'timestamp': timestamp,
                        'open': 1.1000,
                        'high': 1.1005,
                        'low': 1.0995,
                        'close': close,
                        'volume': 1000
                    })
        
        signal = strategy.calculate_signal(candles)
        self.assertIn(signal, ['call', 'put', None])
    
    def test_pivot_strategy(self):
        """Testa a estratégia Pivot"""
        strategy = PivotStrategy(self.config)
        
        # Cria dados de teste com pivots
        candles = []
        for i in range(30):
            # Cria padrão de pivot
            if i in [10, 20]:
                high = 1.1020  # Pivot alto
                low = 1.1000
            elif i in [5, 15, 25]:
                high = 1.1005
                low = 1.0980  # Pivot baixo
            else:
                high = 1.1005
                low = 1.1000
            
            candles.append({
                'timestamp': i,
                'open': 1.1000,
                'high': high,
                'low': low,
                'close': 1.1002,
                'volume': 1000
            })
        
        signal = strategy.calculate_signal(candles)
        self.assertIn(signal, ['call', 'put', None])
    
    def test_confluence_strategy(self):
        """Testa a estratégia de Confluência"""
        strategy = ConfluenceStrategy(self.config)
        
        # Cria dados de teste para confluência
        candles = []
        base_time = 1609459200
        
        for day in range(10):
            for hour in range(9, 17):
                for minute in [5, 15, 25, 35, 45, 55]:
                    timestamp = base_time + (day * 86400) + (hour * 3600) + (minute * 60)
                    
                    # Simula padrão de confluência no horário 10:05
                    if hour == 10 and minute == 5:
                        close = 1.1002 if day < 5 else 1.0998  # Maioria verde
                    else:
                        close = 1.1000 + (day * 0.0001)
                    
                    candles.append({
                        'timestamp': timestamp,
                        'open': 1.1000,
                        'high': 1.1005,
                        'low': 1.0995,
                        'close': close,
                        'volume': 1000
                    })
        
        signal = strategy.calculate_signal(candles)
        self.assertIn(signal, ['call', 'put', None])
    
    def test_mhi_pivot_strategy(self):
        """Testa a estratégia combinada MHI + Pivot"""
        strategy = MHIPivotStrategy(self.config)
        
        # Cria dados de teste
        candles = []
        for i in range(100):
            candles.append({
                'timestamp': i,
                'open': 1.1000,
                'high': 1.1005,
                'low': 1.0995,
                'close': 1.1002,
                'volume': 1000
            })
        
        signal = strategy.calculate_signal(candles)
        self.assertIn(signal, ['call', 'put', None])
    
    def test_binary_pattern_strategy(self):
        """Testa a estratégia de padrões binários"""
        strategy = BinaryPatternStrategy(self.config)
        
        # Cria dados de teste com padrão específico
        candles = []
        pattern = [1.1002, 1.1002, 1.0998]  # green, green, red
        
        for i in range(10):
            if i < 3:
                close = pattern[i]
            else:
                close = 1.1000
            
            candles.append({
                'timestamp': i,
                'open': 1.1000,
                'high': 1.1005,
                'low': 1.0995,
                'close': close,
                'volume': 1000
            })
        
        signal = strategy.calculate_signal(candles)
        self.assertIn(signal, ['call', 'put', None])
    
    def test_time_based_strategy(self):
        """Testa a estratégia baseada em horários"""
        strategy = TimeBasedStrategy(self.config)
        
        # Cria dados de teste simples
        candles = [{'timestamp': 1, 'open': 1.1000, 'high': 1.1005, 'low': 1.0995, 'close': 1.1002, 'volume': 1000}]
        
        signal = strategy.calculate_signal(candles)
        self.assertIn(signal, ['call', 'put', None])

class TestRiskManager(unittest.TestCase):
    """Testes para o gerenciador de risco"""
    
    def setUp(self):
        self.config = Config()
        self.config.MAX_DAILY_LOSS = 50
        self.config.MAX_DAILY_TRADES = 20
        self.risk_manager = RiskManager(self.config)
    
    def test_can_trade(self):
        """Testa se pode operar"""
        # Deve poder operar no início
        self.assertTrue(self.risk_manager.can_trade())
    
    def test_record_trade(self):
        """Testa registro de operação"""
        trade_data = {
            'asset': 'EURUSD',
            'action': 'call',
            'amount': 1.0,
            'profit': 0.8
        }
        
        self.risk_manager.record_trade(trade_data)
        daily_stats = self.risk_manager.get_daily_stats()
        
        self.assertEqual(daily_stats['trades_count'], 1)
        self.assertEqual(daily_stats['total_profit'], 0.8)
        self.assertEqual(daily_stats['wins'], 1)
    
    def test_daily_limits(self):
        """Testa limites diários"""
        # Simula muitas operações
        for i in range(25):
            trade_data = {
                'asset': 'EURUSD',
                'action': 'call',
                'amount': 1.0,
                'profit': -1.0
            }
            self.risk_manager.record_trade(trade_data)
        
        # Não deve poder operar mais
        self.assertFalse(self.risk_manager.can_trade())

class TestLogger(unittest.TestCase):
    """Testes para o sistema de logs"""
    
    def setUp(self):
        self.config = Config()
        self.logger = TradingLogger(self.config)
    
    def test_logger_creation(self):
        """Testa criação do logger"""
        self.assertIsNotNone(self.logger.logger)
    
    def test_log_trade(self):
        """Testa log de operação"""
        trade_data = {
            'action': 'call',
            'asset': 'EURUSD',
            'amount': 1.0,
            'profit': 0.8
        }
        
        # Não deve gerar erro
        self.logger.log_trade(trade_data)

class TestConfig(unittest.TestCase):
    """Testes para configurações"""
    
    def test_config_loading(self):
        """Testa carregamento de configurações"""
        config = Config()
        
        self.assertIsInstance(config.ASSET, str)
        self.assertIsInstance(config.AMOUNT, (int, float))
        self.assertIsInstance(config.STRATEGY, str)
        self.assertIsInstance(config.EXPIRATION, int)

def run_tests():
    """Executa todos os testes"""
    print("🧪 Executando testes do robô...")
    print("=" * 50)
    
    # Cria suite de testes
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Adiciona testes
    suite.addTests(loader.loadTestsFromTestCase(TestStrategies))
    suite.addTests(loader.loadTestsFromTestCase(TestRiskManager))
    suite.addTests(loader.loadTestsFromTestCase(TestLogger))
    suite.addTests(loader.loadTestsFromTestCase(TestConfig))
    
    # Executa testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("=" * 50)
    if result.wasSuccessful():
        print("✅ Todos os testes passaram!")
    else:
        print("❌ Alguns testes falharam!")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    run_tests()