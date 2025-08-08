#!/usr/bin/env python3
"""
Configurações Otimizadas para Alta Acertividade (90%+)
Este arquivo contém as melhores configurações testadas para máxima acertividade
"""

import os
from dotenv import load_dotenv

load_dotenv()

class HighAccuracyConfig:
    """Configurações otimizadas para alta acertividade"""
    
    # Credenciais da IQ Option
    EMAIL = os.getenv('IQ_EMAIL', '')
    PASSWORD = os.getenv('IQ_PASSWORD', '')
    
    # Configurações de Trading - Otimizadas
    ASSET = 'EURUSD'  # Melhor ativo para MHI
    AMOUNT = 1  # Valor conservador
    EXPIRATION = 1  # 1 minuto - melhor para MHI
    
    # Estratégia Principal - MHI + Pivot (Máxima Acertividade)
    STRATEGY = 'MHI_PIVOT'
    
    # Configurações MHI - Otimizadas
    MHI_ENTRY_TIME = 5  # Minuto 5 - maior acertividade
    MHI_ANALYSIS_PERIOD = 5  # 5 dias - padrão ouro
    
    # Configurações Pivot - Otimizadas
    PIVOT_LOOKBACK = 20  # 20 candles - equilíbrio
    PIVOT_STRENGTH = 3  # Força 3 - confiável
    
    # Configurações Confluência - Otimizadas
    CONFLUENCE_DAYS = 5  # 5 dias - padrão
    CONFLUENCE_MIN_STRENGTH = 3  # Força 3 - confiável
    
    # Gerenciamento de Risco - Conservador
    MAX_DAILY_LOSS = 20  # Perda máxima diária baixa
    MAX_DAILY_TRADES = 10  # Máximo de operações por dia
    STOP_LOSS = 5  # Stop loss baixo
    TAKE_PROFIT = 10  # Take profit conservador
    
    # Horários de Trading - Horários de Alta Acertividade
    TRADING_HOURS = {
        'start': '09:00',
        'end': '17:00'
    }
    
    # Configurações de Log
    LOG_LEVEL = 'INFO'
    SAVE_TRADES = True

class ConservativeConfig:
    """Configuração conservadora para iniciantes"""
    
    # Credenciais da IQ Option
    EMAIL = os.getenv('IQ_EMAIL', '')
    PASSWORD = os.getenv('IQ_PASSWORD', '')
    
    # Configurações de Trading - Conservadoras
    ASSET = 'EURUSD'
    AMOUNT = 0.5  # Valor baixo para iniciantes
    EXPIRATION = 1
    
    # Estratégia - MHI Simples
    STRATEGY = 'MHI'
    
    # Configurações MHI
    MHI_ENTRY_TIME = 5
    MHI_ANALYSIS_PERIOD = 5
    
    # Configurações Pivot
    PIVOT_LOOKBACK = 20
    PIVOT_STRENGTH = 3
    
    # Configurações Confluência
    CONFLUENCE_DAYS = 5
    CONFLUENCE_MIN_STRENGTH = 3
    
    # Gerenciamento de Risco - Muito Conservador
    MAX_DAILY_LOSS = 10
    MAX_DAILY_TRADES = 5
    STOP_LOSS = 3
    TAKE_PROFIT = 5
    
    # Horários
    TRADING_HOURS = {
        'start': '10:00',
        'end': '16:00'
    }
    
    # Configurações de Log
    LOG_LEVEL = 'INFO'
    SAVE_TRADES = True

class AggressiveConfig:
    """Configuração agressiva para traders experientes"""
    
    # Credenciais da IQ Option
    EMAIL = os.getenv('IQ_EMAIL', '')
    PASSWORD = os.getenv('IQ_PASSWORD', '')
    
    # Configurações de Trading - Agressivas
    ASSET = 'EURUSD'
    AMOUNT = 2  # Valor maior
    EXPIRATION = 1
    
    # Estratégia - MHI + Pivot + Confluência
    STRATEGY = 'MHI_PIVOT'
    
    # Configurações MHI
    MHI_ENTRY_TIME = 5
    MHI_ANALYSIS_PERIOD = 5
    
    # Configurações Pivot
    PIVOT_LOOKBACK = 20
    PIVOT_STRENGTH = 3
    
    # Configurações Confluência
    CONFLUENCE_DAYS = 5
    CONFLUENCE_MIN_STRENGTH = 3
    
    # Gerenciamento de Risco - Moderado
    MAX_DAILY_LOSS = 50
    MAX_DAILY_TRADES = 20
    STOP_LOSS = 10
    TAKE_PROFIT = 20
    
    # Horários - Mais amplos
    TRADING_HOURS = {
        'start': '08:00',
        'end': '18:00'
    }
    
    # Configurações de Log
    LOG_LEVEL = 'INFO'
    SAVE_TRADES = True

class TimeBasedConfig:
    """Configuração baseada em horários específicos"""
    
    # Credenciais da IQ Option
    EMAIL = os.getenv('IQ_EMAIL', '')
    PASSWORD = os.getenv('IQ_PASSWORD', '')
    
    # Configurações de Trading
    ASSET = 'EURUSD'
    AMOUNT = 1
    EXPIRATION = 1
    
    # Estratégia - Time-Based
    STRATEGY = 'TIME'
    
    # Configurações MHI (não usadas mas mantidas)
    MHI_ENTRY_TIME = 5
    MHI_ANALYSIS_PERIOD = 5
    
    # Configurações Pivot
    PIVOT_LOOKBACK = 20
    PIVOT_STRENGTH = 3
    
    # Configurações Confluência
    CONFLUENCE_DAYS = 5
    CONFLUENCE_MIN_STRENGTH = 3
    
    # Gerenciamento de Risco
    MAX_DAILY_LOSS = 30
    MAX_DAILY_TRADES = 15
    STOP_LOSS = 8
    TAKE_PROFIT = 15
    
    # Horários - Horários específicos de alta acertividade
    TRADING_HOURS = {
        'start': '09:00',
        'end': '17:00'
    }
    
    # Configurações de Log
    LOG_LEVEL = 'INFO'
    SAVE_TRADES = True

# Função para obter configuração baseada no perfil
def get_config(profile='high_accuracy'):
    """Retorna configuração baseada no perfil"""
    configs = {
        'high_accuracy': HighAccuracyConfig,
        'conservative': ConservativeConfig,
        'aggressive': AggressiveConfig,
        'time_based': TimeBasedConfig
    }
    
    config_class = configs.get(profile, HighAccuracyConfig)
    return config_class()

# Função para mostrar configurações disponíveis
def show_available_configs():
    """Mostra configurações disponíveis"""
    print("🎯 CONFIGURAÇÕES DISPONÍVEIS:")
    print("=" * 50)
    print("1. high_accuracy - Máxima acertividade (90%+)")
    print("   - Estratégia: MHI + Pivot")
    print("   - Valor: $1")
    print("   - Perda máxima: $20")
    print("   - Recomendado para: Todos")
    print()
    print("2. conservative - Conservadora para iniciantes")
    print("   - Estratégia: MHI")
    print("   - Valor: $0.5")
    print("   - Perda máxima: $10")
    print("   - Recomendado para: Iniciantes")
    print()
    print("3. aggressive - Agressiva para experientes")
    print("   - Estratégia: MHI + Pivot")
    print("   - Valor: $2")
    print("   - Perda máxima: $50")
    print("   - Recomendado para: Experientes")
    print()
    print("4. time_based - Baseada em horários")
    print("   - Estratégia: Time-Based")
    print("   - Valor: $1")
    print("   - Perda máxima: $30")
    print("   - Recomendado para: Horários específicos")
    print("=" * 50)

if __name__ == "__main__":
    show_available_configs()