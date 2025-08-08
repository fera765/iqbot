#!/usr/bin/env python3
"""
Testes para o Robô de Trading IQ Option
"""

import unittest
from unittest.mock import Mock, patch
import pandas as pd
import numpy as np

from config import Config
from strategies import RSIStrategy, MACDStrategy, BollingerBandsStrategy, RandomStrategy
from risk_manager import RiskManager
from logger import TradingLogger

class TestStrategies(unittest.TestCase):
    """Testes para as estratégias de trading"""
    
    def setUp(self):
        self.config = Config()
        self.config.STRATEGY = 'RSI'
        self.config.RSI_PERIOD = 14
        self.config.RSI_OVERBOUGHT = 70
        self.config.RSI_OVERSOLD = 30
    
    def test_rsi_strategy(self):
        """Testa a estratégia RSI"""
        strategy = RSIStrategy(self.config)
        
        # Cria dados de teste
        candles = []
        for i in range(20):
            candles.append({
                'timestamp': i,
                'open': 1.1000 + i * 0.0001,
                'high': 1.1005 + i * 0.0001,
                'low': 1.0995 + i * 0.0001,
                'close': 1.1002 + i * 0.0001,
                'volume': 1000
            })
        
        # Testa cálculo de RSI
        df = strategy.get_candles_dataframe(candles)
        prices = df['close'].tolist()
        rsi = strategy.calculate_rsi(prices, 14)
        
        self.assertIsInstance(rsi, float)
        self.assertGreaterEqual(rsi, 0)
        self.assertLessEqual(rsi, 100)
    
    def test_macd_strategy(self):
        """Testa a estratégia MACD"""
        strategy = MACDStrategy(self.config)
        
        # Cria dados de teste
        candles = []
        for i in range(50):
            candles.append({
                'timestamp': i,
                'open': 1.1000 + i * 0.0001,
                'high': 1.1005 + i * 0.0001,
                'low': 1.0995 + i * 0.0001,
                'close': 1.1002 + i * 0.0001,
                'volume': 1000
            })
        
        signal = strategy.calculate_signal(candles)
        # MACD pode retornar None se não houver sinal claro
        self.assertIn(signal, ['call', 'put', None])
    
    def test_bollinger_strategy(self):
        """Testa a estratégia Bandas de Bollinger"""
        strategy = BollingerBandsStrategy(self.config)
        
        # Cria dados de teste
        candles = []
        for i in range(30):
            candles.append({
                'timestamp': i,
                'open': 1.1000 + i * 0.0001,
                'high': 1.1005 + i * 0.0001,
                'low': 1.0995 + i * 0.0001,
                'close': 1.1002 + i * 0.0001,
                'volume': 1000
            })
        
        signal = strategy.calculate_signal(candles)
        self.assertIn(signal, ['call', 'put', None])
    
    def test_random_strategy(self):
        """Testa a estratégia Random"""
        strategy = RandomStrategy(self.config)
        
        # Cria dados de teste
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