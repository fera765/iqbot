#!/usr/bin/env python3
"""
Exemplos de uso do Robô IQ Option
"""

from config import Config
from trading_bot import IQOptionBot
from strategies import MHIStrategy, PivotStrategy, ConfluenceStrategy, MHIPivotStrategy, BinaryPatternStrategy, TimeBasedStrategy
from risk_manager import RiskManager
from logger import TradingLogger

def exemplo_configuracao_basica():
    """Exemplo de configuração básica"""
    print("=== EXEMPLO 1: Configuração Básica ===")
    
    # Configurações padrão
    config = Config()
    config.ASSET = 'EURUSD'
    config.AMOUNT = 1
    config.STRATEGY = 'MHI'
    config.EXPIRATION = 1
    
    print(f"Ativo: {config.ASSET}")
    print(f"Valor: ${config.AMOUNT}")
    print(f"Estratégia: {config.STRATEGY}")
    print(f"Expiração: {config.EXPIRATION} min")

def exemplo_estrategias():
    """Exemplo de uso das estratégias"""
    print("\n=== EXEMPLO 2: Testando Estratégias ===")
    
    config = Config()
    
    # Testa MHI
    mhi_strategy = MHIStrategy(config)
    print(f"MHI Strategy: {mhi_strategy.name}")
    
    # Testa Pivot
    pivot_strategy = PivotStrategy(config)
    print(f"Pivot Strategy: {pivot_strategy.name}")
    
    # Testa Confluência
    confluence_strategy = ConfluenceStrategy(config)
    print(f"Confluence Strategy: {confluence_strategy.name}")
    
    # Testa MHI + Pivot
    mhi_pivot_strategy = MHIPivotStrategy(config)
    print(f"MHI + Pivot Strategy: {mhi_pivot_strategy.name}")
    
    # Testa Padrões Binários
    binary_strategy = BinaryPatternStrategy(config)
    print(f"Binary Pattern Strategy: {binary_strategy.name}")
    
    # Testa Time-Based
    time_strategy = TimeBasedStrategy(config)
    print(f"Time-Based Strategy: {time_strategy.name}")

def exemplo_gerenciamento_risco():
    """Exemplo de gerenciamento de risco"""
    print("\n=== EXEMPLO 3: Gerenciamento de Risco ===")
    
    config = Config()
    config.MAX_DAILY_LOSS = 20
    config.MAX_DAILY_TRADES = 10
    
    risk_manager = RiskManager(config)
    
    # Simula algumas operações
    trades = [
        {'asset': 'EURUSD', 'action': 'call', 'amount': 1, 'profit': 0.8},
        {'asset': 'EURUSD', 'action': 'put', 'amount': 1, 'profit': -1.0},
        {'asset': 'EURUSD', 'action': 'call', 'amount': 1, 'profit': 0.8},
    ]
    
    for trade in trades:
        risk_manager.record_trade(trade)
        stats = risk_manager.get_daily_stats()
        print(f"Trades: {stats['trades_count']}, Profit: ${stats['total_profit']:.2f}")
    
    print(f"Pode operar: {risk_manager.can_trade()}")

def exemplo_logger():
    """Exemplo de uso do logger"""
    print("\n=== EXEMPLO 4: Sistema de Logs ===")
    
    config = Config()
    logger = TradingLogger(config)
    
    logger.info("Iniciando exemplo de logs")
    logger.warning("Este é um aviso")
    logger.error("Este é um erro")
    
    # Log de operação
    trade_data = {
        'action': 'call',
        'asset': 'EURUSD',
        'amount': 1.0,
        'profit': 0.8
    }
    logger.log_trade(trade_data)

def exemplo_backtest():
    """Exemplo de backtest"""
    print("\n=== EXEMPLO 5: Backtest ===")
    
    config = Config()
    config.ASSET = 'EURUSD'
    config.AMOUNT = 1
    config.STRATEGY = 'MHI_PIVOT'
    
    bot = IQOptionBot(config)
    
    print("Executando backtest de 3 dias...")
    bot.run_backtest(3)

def exemplo_configuracao_avancada():
    """Exemplo de configuração avançada"""
    print("\n=== EXEMPLO 6: Configuração Avançada ===")
    
    config = Config()
    
    # Configuração para alta acertividade
    config.ASSET = 'EURUSD'
    config.AMOUNT = 1
    config.STRATEGY = 'MHI_PIVOT'
    config.EXPIRATION = 1
    config.MHI_ENTRY_TIME = 5
    config.MHI_ANALYSIS_PERIOD = 5
    config.PIVOT_LOOKBACK = 20
    config.PIVOT_STRENGTH = 3
    config.CONFLUENCE_DAYS = 5
    config.CONFLUENCE_MIN_STRENGTH = 3
    config.MAX_DAILY_LOSS = 20
    config.MAX_DAILY_TRADES = 10
    config.TRADING_HOURS = {'start': '09:00', 'end': '17:00'}
    
    print("Configuração para Alta Acertividade:")
    print(f"- Ativo: {config.ASSET}")
    print(f"- Valor: ${config.AMOUNT}")
    print(f"- Estratégia: {config.STRATEGY}")
    print(f"- Expiração: {config.EXPIRATION} min")
    print(f"- Horário MHI: {config.MHI_ENTRY_TIME} min")
    print(f"- Análise MHI: {config.MHI_ANALYSIS_PERIOD} dias")
    print(f"- Lookback Pivot: {config.PIVOT_LOOKBACK} candles")
    print(f"- Força Pivot: {config.PIVOT_STRENGTH}")
    print(f"- Dias Confluência: {config.CONFLUENCE_DAYS}")
    print(f"- Força Confluência: {config.CONFLUENCE_MIN_STRENGTH}")
    print(f"- Perda máxima: ${config.MAX_DAILY_LOSS}")
    print(f"- Máximo trades: {config.MAX_DAILY_TRADES}")
    print(f"- Horário: {config.TRADING_HOURS['start']} - {config.TRADING_HOURS['end']}")

def exemplo_estatisticas():
    """Exemplo de análise de estatísticas"""
    print("\n=== EXEMPLO 7: Análise de Estatísticas ===")
    
    config = Config()
    risk_manager = RiskManager(config)
    
    # Simula histórico de operações
    historical_trades = [
        {'profit': 0.8}, {'profit': -1.0}, {'profit': 0.8},
        {'profit': 0.8}, {'profit': -1.0}, {'profit': 0.8},
        {'profit': -1.0}, {'profit': 0.8}, {'profit': 0.8},
        {'profit': -1.0}
    ]
    
    for trade in historical_trades:
        risk_manager.record_trade(trade)
    
    # Análise
    total_stats = risk_manager.get_total_stats()
    
    print("Estatísticas Totais:")
    print(f"- Total de operações: {total_stats['total_trades']}")
    print(f"- Lucro total: ${total_stats['total_profit']:.2f}")
    print(f"- Vitórias: {total_stats['wins']}")
    print(f"- Derrotas: {total_stats['losses']}")
    print(f"- Taxa de acerto: {total_stats['win_rate']:.1f}%")

def main():
    """Executa todos os exemplos"""
    print("🤖 EXEMPLOS DO ROBÔ IQ OPTION")
    print("=" * 50)
    
    try:
        exemplo_configuracao_basica()
        exemplo_estrategias()
        exemplo_gerenciamento_risco()
        exemplo_logger()
        exemplo_backtest()
        exemplo_configuracao_avancada()
        exemplo_estatisticas()
        
        print("\n" + "=" * 50)
        print("✅ Todos os exemplos executados com sucesso!")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Erro ao executar exemplos: {str(e)}")

if __name__ == "__main__":
    main()