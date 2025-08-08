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
from trading_bot import IQOptionBot

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description='IQ Option Trading Bot')
    parser.add_argument('--mode', choices=['live', 'backtest'], default='live',
                       help='Modo de execução: live (real) ou backtest (simulação)')
    parser.add_argument('--days', type=int, default=7,
                       help='Número de dias para backtest (apenas no modo backtest)')
    parser.add_argument('--config', type=str, default='config.py',
                       help='Arquivo de configuração')
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("🤖 IQ OPTION TRADING BOT")
    print("=" * 50)
    print(f"Modo: {args.mode.upper()}")
    print(f"Ativo: {Config.ASSET}")
    print(f"Estratégia: {Config.STRATEGY}")
    print(f"Valor por operação: ${Config.AMOUNT}")
    print(f"Expiração: {Config.EXPIRATION} min")
    print("=" * 50)
    
    # Verifica credenciais
    if not Config.EMAIL or not Config.PASSWORD:
        print("❌ ERRO: Credenciais não configuradas!")
        print("Configure suas credenciais no arquivo .env:")
        print("IQ_EMAIL=seu_email@exemplo.com")
        print("IQ_PASSWORD=sua_senha")
        sys.exit(1)
    
    # Cria instância do robô
    bot = IQOptionBot(Config)
    
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