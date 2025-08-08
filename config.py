import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Credenciais da IQ Option
    EMAIL = os.getenv('IQ_EMAIL', '')
    PASSWORD = os.getenv('IQ_PASSWORD', '')
    
    # Configurações de Trading
    ASSET = 'EURUSD'  # Ativo para operar
    AMOUNT = 1  # Valor em dólares para cada operação
    EXPIRATION = 1  # Tempo de expiração em minutos (1 ou 5)
    
    # Configurações de Estratégia
    STRATEGY = 'MHI'  # Estratégia: MHI, PIVOT, CONFLUENCE, MHI_PIVOT
    MHI_ENTRY_TIME = 5  # Minuto de entrada MHI (5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55)
    MHI_ANALYSIS_PERIOD = 5  # Dias para análise MHI
    
    # Configurações de Pivot
    PIVOT_LOOKBACK = 20  # Candles para análise de pivot
    PIVOT_STRENGTH = 3  # Força mínima do pivot (1-5)
    
    # Configurações de Confluência
    CONFLUENCE_DAYS = 5  # Dias para análise de confluência
    CONFLUENCE_MIN_STRENGTH = 3  # Força mínima da confluência
    
    # Configurações de Gerenciamento de Risco
    MAX_DAILY_LOSS = 50  # Perda máxima diária em dólares
    MAX_DAILY_TRADES = 20  # Máximo de operações por dia
    STOP_LOSS = 10  # Stop loss em dólares
    TAKE_PROFIT = 15  # Take profit em dólares
    
    # Configurações de Horário
    TRADING_HOURS = {
        'start': '09:00',
        'end': '17:00'
    }
    
    # Configurações de Log
    LOG_LEVEL = 'INFO'
    SAVE_TRADES = True