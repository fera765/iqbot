#!/usr/bin/env python3
"""
Robô de Trading IQ Option
Autor: AI Assistant
Versão: 1.0.0

Este robô automatiza operações na IQ Option usando diferentes estratégias
de análise técnica como RSI, MACD e Bandas de Bollinger.
"""

import sys
import argparse
from config import Config
from high_accuracy_config import get_config, show_available_configs
from trading_bot import IQOptionBot

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description='IQ Option Trading Bot')
    parser.add_argument('--mode', choices=['live', 'backtest'], default='live',
                       help='Modo de execução: live (real) ou backtest (simulação)')
    parser.add_argument('--days', type=int, default=7,
                       help='Número de dias para backtest (apenas no modo backtest)')
    parser.add_argument('--profile', type=str, 
                       choices=['high_accuracy', 'conservative', 'aggressive', 'time_based'],
                       default='high_accuracy',
                       help='Perfil de configuração para alta acertividade')
    parser.add_argument('--show-configs', action='store_true',
                       help='Mostra configurações disponíveis')
    
    args = parser.parse_args()
    
    # Mostra configurações disponíveis se solicitado
    if args.show_configs:
        show_available_configs()
        sys.exit(0)
    
    # Obtém configuração baseada no perfil
    config = get_config(args.profile)
    
    print("=" * 50)
    print("🤖 IQ OPTION TRADING BOT - ALTA ACERTIVIDADE")
    print("=" * 50)
    print(f"Modo: {args.mode.upper()}")
    print(f"Perfil: {args.profile}")
    print(f"Ativo: {config.ASSET}")
    print(f"Estratégia: {config.STRATEGY}")
    print(f"Valor por operação: ${config.AMOUNT}")
    print(f"Expiração: {config.EXPIRATION} min")
    print(f"Horário MHI: {config.MHI_ENTRY_TIME} min")
    print(f"Análise MHI: {config.MHI_ANALYSIS_PERIOD} dias")
    print(f"Perda máxima: ${config.MAX_DAILY_LOSS}")
    print(f"Máximo trades: {config.MAX_DAILY_TRADES}")
    print("=" * 50)
    
    # Verifica credenciais
    if not config.EMAIL or not config.PASSWORD:
        print("❌ ERRO: Credenciais não configuradas!")
        print("Configure suas credenciais no arquivo .env:")
        print("IQ_EMAIL=seu_email@exemplo.com")
        print("IQ_PASSWORD=sua_senha")
        sys.exit(1)
    
    # Cria instância do robô
    bot = IQOptionBot(config)
    
    try:
        if args.mode == 'live':
            print("🚀 Iniciando robô em modo LIVE...")
            print("⚠️  ATENÇÃO: Este modo fará operações reais com dinheiro!")
            print("Pressione Ctrl+C para parar o robô")
            print("-" * 50)
            
            # Executa o robô
            bot.run()
            
        elif args.mode == 'backtest':
            print(f"🧪 Iniciando BACKTEST por {args.days} dias...")
            print("Este modo simula operações sem usar dinheiro real")
            print("-" * 50)
            
            # Executa backtest
            bot.run_backtest(args.days)
    
    except KeyboardInterrupt:
        print("\n⏹️  Robô interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")
    finally:
        print("👋 Robô finalizado")

if __name__ == "__main__":
    main()