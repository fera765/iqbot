import time
import threading
from datetime import datetime, time as dt_time
from typing import Dict, List, Optional

from iqoptionapi.stable_api import IQ_Option
from config import Config
from strategies import get_strategy
from risk_manager import RiskManager
from logger import TradingLogger

class IQOptionBot:
    """Robô de trading para IQ Option"""
    
    def __init__(self, config: Config):
        self.config = config
        self.api = IQ_Option(config.EMAIL, config.PASSWORD)
        self.strategy = get_strategy(config)
        self.risk_manager = RiskManager(config)
        self.logger = TradingLogger(config)
        
        self.is_running = False
        self.is_connected = False
        self.current_balance = 0.0
        self.active_trades = {}
        
    def connect(self) -> bool:
        """Conecta à IQ Option"""
        try:
            self.logger.info("Connecting to IQ Option...")
            
            # Conecta à API
            status = self.api.connect()
            
            if status:
                self.is_connected = True
                self.logger.log_connection(True)
                
                # Obtém informações da conta
                self.current_balance = self.api.get_balance()
                self.logger.log_balance(self.current_balance)
                
                # Obtém informações do perfil
                profile = self.api.get_profile()
                self.logger.info(f"Logged in as: {profile.get('name', 'Unknown')}")
                
                return True
            else:
                self.logger.log_connection(False)
                return False
                
        except Exception as e:
            self.logger.error(f"Connection error: {str(e)}")
            return False
    
    def disconnect(self):
        """Desconecta da IQ Option"""
        if self.is_connected:
            self.api.close_connection()
            self.is_connected = False
            self.logger.info("Disconnected from IQ Option")
    
    def get_candles(self, asset: str, count: int = 100) -> List[Dict]:
        """Obtém candles do ativo"""
        try:
            # Obtém candles de 1 minuto
            candles = self.api.get_candles(asset, 60, count, time.time())
            return candles
        except Exception as e:
            self.logger.error(f"Error getting candles: {str(e)}")
            return []
    
    def place_trade(self, asset: str, action: str, amount: float, expiration: int) -> Optional[int]:
        """Coloca uma ordem de trading"""
        try:
            # Verifica se pode operar
            if not self.risk_manager.can_trade():
                self.logger.warning("Cannot place trade - risk limits reached")
                return None
            
            # Coloca a ordem
            order_id = self.api.buy(amount, asset, action, expiration)
            
            if order_id:
                self.logger.info(f"Order placed: {action.upper()} {asset} | Amount: ${amount} | ID: {order_id}")
                
                # Registra a ordem ativa
                self.active_trades[order_id] = {
                    'asset': asset,
                    'action': action,
                    'amount': amount,
                    'expiration': expiration,
                    'timestamp': datetime.now().isoformat()
                }
                
                return order_id
            else:
                self.logger.error(f"Failed to place order: {action} {asset}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error placing trade: {str(e)}")
            return None
    
    def check_trade_result(self, order_id: int) -> Optional[Dict]:
        """Verifica o resultado de uma operação"""
        try:
            # Verifica se a ordem foi finalizada
            if self.api.check_win_v4(order_id):
                profit = self.api.get_async_order(order_id)['win']
                result = 'win'
            elif self.api.check_win_v4(order_id) is False:
                profit = -self.active_trades[order_id]['amount']
                result = 'loss'
            else:
                # Ordem ainda não finalizada
                return None
            
            # Remove da lista de ordens ativas
            trade_data = self.active_trades.pop(order_id, {})
            
            # Prepara dados da operação
            trade_result = {
                'order_id': order_id,
                'asset': trade_data.get('asset', ''),
                'action': trade_data.get('action', ''),
                'amount': trade_data.get('amount', 0),
                'profit': profit,
                'result': result,
                'timestamp': datetime.now().isoformat()
            }
            
            # Registra no gerenciador de risco
            self.risk_manager.record_trade(trade_result)
            
            # Log do resultado
            self.logger.log_trade(trade_result)
            
            return trade_result
            
        except Exception as e:
            self.logger.error(f"Error checking trade result: {str(e)}")
            return None
    
    def check_active_trades(self):
        """Verifica todas as ordens ativas"""
        completed_trades = []
        
        for order_id in list(self.active_trades.keys()):
            result = self.check_trade_result(order_id)
            if result:
                completed_trades.append(result)
        
        return completed_trades
    
    def should_trade_now(self) -> bool:
        """Verifica se deve operar agora baseado no horário"""
        now = datetime.now().time()
        start_time = dt_time.fromisoformat(self.config.TRADING_HOURS['start'])
        end_time = dt_time.fromisoformat(self.config.TRADING_HOURS['end'])
        
        return start_time <= now <= end_time
    
    def trading_cycle(self):
        """Ciclo principal de trading"""
        try:
            # Verifica se deve operar
            if not self.should_trade_now():
                self.logger.debug("Outside trading hours")
                return
            
            # Verifica limites de risco
            if self.risk_manager.should_stop_trading():
                self.logger.warning("Trading stopped due to risk limits")
                return
            
            # Obtém candles
            candles = self.get_candles(self.config.ASSET, 100)
            if not candles:
                self.logger.warning("No candles available")
                return
            
            # Calcula sinal
            signal = self.strategy.calculate_signal(candles)
            
            if signal:
                self.logger.log_signal(signal, self.config.ASSET, self.strategy.name)
                
                # Coloca ordem
                order_id = self.place_trade(
                    self.config.ASSET,
                    signal,
                    self.config.AMOUNT,
                    self.config.EXPIRATION
                )
                
                if order_id:
                    self.logger.info(f"Trade placed successfully: {signal.upper()} {self.config.ASSET}")
                else:
                    self.logger.error("Failed to place trade")
            else:
                self.logger.debug("No signal generated")
                
        except Exception as e:
            self.logger.error(f"Error in trading cycle: {str(e)}")
    
    def run(self):
        """Executa o robô"""
        if not self.connect():
            self.logger.critical("Failed to connect to IQ Option. Exiting.")
            return
        
        self.is_running = True
        self.logger.info("Trading bot started")
        
        try:
            while self.is_running:
                # Verifica ordens ativas
                self.check_active_trades()
                
                # Executa ciclo de trading
                self.trading_cycle()
                
                # Mostra estatísticas
                daily_stats = self.risk_manager.get_daily_stats()
                if daily_stats['trades_count'] > 0:
                    self.logger.log_stats(daily_stats)
                
                # Aguarda próximo ciclo
                time.sleep(60)  # 1 minuto
                
        except KeyboardInterrupt:
            self.logger.info("Bot stopped by user")
        except Exception as e:
            self.logger.critical(f"Unexpected error: {str(e)}")
        finally:
            self.stop()
    
    def stop(self):
        """Para o robô"""
        self.is_running = False
        self.disconnect()
        
        # Mostra estatísticas finais
        total_stats = self.risk_manager.get_total_stats()
        self.logger.info("=== FINAL STATISTICS ===")
        self.logger.info(f"Total Trades: {total_stats['total_trades']}")
        self.logger.info(f"Total Profit: ${total_stats['total_profit']:.2f}")
        self.logger.info(f"Win Rate: {total_stats['win_rate']:.1f}%")
        self.logger.info("Bot stopped")
    
    def run_backtest(self, days: int = 7):
        """Executa backtest (simulação)"""
        self.logger.info(f"Starting backtest for {days} days")
        
        # Simula operações
        for day in range(days):
            self.logger.info(f"Backtest day {day + 1}")
            
            # Simula algumas operações por dia
            for trade in range(5):
                # Simula resultado aleatório
                profit = (1 if trade % 2 == 0 else -1) * self.config.AMOUNT * 0.8
                
                trade_data = {
                    'asset': self.config.ASSET,
                    'action': 'call' if trade % 2 == 0 else 'put',
                    'amount': self.config.AMOUNT,
                    'profit': profit,
                    'result': 'win' if profit > 0 else 'loss'
                }
                
                self.risk_manager.record_trade(trade_data)
                self.logger.log_trade(trade_data)
                
                time.sleep(0.1)  # Pequena pausa
        
        # Mostra resultados do backtest
        total_stats = self.risk_manager.get_total_stats()
        self.logger.info("=== BACKTEST RESULTS ===")
        self.logger.info(f"Total Trades: {total_stats['total_trades']}")
        self.logger.info(f"Total Profit: ${total_stats['total_profit']:.2f}")
        self.logger.info(f"Win Rate: {total_stats['win_rate']:.1f}%")