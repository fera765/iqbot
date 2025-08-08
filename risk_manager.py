import json
import os
from datetime import datetime, date
from typing import Dict, List

class RiskManager:
    """Gerenciador de risco para controlar perdas e operações"""
    
    def __init__(self, config):
        self.config = config
        self.daily_stats_file = 'daily_stats.json'
        self.trades_file = 'trades_history.json'
        self.daily_stats = self.load_daily_stats()
        self.trades_history = self.load_trades_history()
    
    def load_daily_stats(self) -> Dict:
        """Carrega estatísticas diárias"""
        if os.path.exists(self.daily_stats_file):
            try:
                with open(self.daily_stats_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def save_daily_stats(self):
        """Salva estatísticas diárias"""
        with open(self.daily_stats_file, 'w') as f:
            json.dump(self.daily_stats, f, indent=2)
    
    def load_trades_history(self) -> List[Dict]:
        """Carrega histórico de operações"""
        if os.path.exists(self.trades_file):
            try:
                with open(self.trades_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def save_trades_history(self):
        """Salva histórico de operações"""
        with open(self.trades_file, 'w') as f:
            json.dump(self.trades_history, f, indent=2)
    
    def get_today_key(self) -> str:
        """Retorna a chave para hoje"""
        return date.today().isoformat()
    
    def can_trade(self) -> bool:
        """Verifica se pode fazer uma nova operação"""
        today = self.get_today_key()
        
        # Inicializa estatísticas do dia se não existir
        if today not in self.daily_stats:
            self.daily_stats[today] = {
                'trades_count': 0,
                'total_profit': 0.0,
                'wins': 0,
                'losses': 0
            }
        
        stats = self.daily_stats[today]
        
        # Verifica limite de operações diárias
        if stats['trades_count'] >= self.config.MAX_DAILY_TRADES:
            return False
        
        # Verifica perda máxima diária
        if stats['total_profit'] <= -self.config.MAX_DAILY_LOSS:
            return False
        
        return True
    
    def record_trade(self, trade_data: Dict):
        """Registra uma operação"""
        today = self.get_today_key()
        
        # Adiciona timestamp se não existir
        if 'timestamp' not in trade_data:
            trade_data['timestamp'] = datetime.now().isoformat()
        
        # Atualiza estatísticas diárias
        if today not in self.daily_stats:
            self.daily_stats[today] = {
                'trades_count': 0,
                'total_profit': 0.0,
                'wins': 0,
                'losses': 0
            }
        
        stats = self.daily_stats[today]
        stats['trades_count'] += 1
        
        profit = trade_data.get('profit', 0.0)
        stats['total_profit'] += profit
        
        if profit > 0:
            stats['wins'] += 1
        elif profit < 0:
            stats['losses'] += 1
        
        # Salva no histórico
        self.trades_history.append(trade_data)
        
        # Salva arquivos
        self.save_daily_stats()
        self.save_trades_history()
    
    def get_daily_stats(self) -> Dict:
        """Retorna estatísticas do dia atual"""
        today = self.get_today_key()
        return self.daily_stats.get(today, {
            'trades_count': 0,
            'total_profit': 0.0,
            'wins': 0,
            'losses': 0
        })
    
    def get_total_stats(self) -> Dict:
        """Retorna estatísticas totais"""
        total_trades = len(self.trades_history)
        total_profit = sum(trade.get('profit', 0) for trade in self.trades_history)
        wins = sum(1 for trade in self.trades_history if trade.get('profit', 0) > 0)
        losses = sum(1 for trade in self.trades_history if trade.get('profit', 0) < 0)
        
        win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
        
        return {
            'total_trades': total_trades,
            'total_profit': total_profit,
            'wins': wins,
            'losses': losses,
            'win_rate': win_rate
        }
    
    def should_stop_trading(self) -> bool:
        """Verifica se deve parar de operar"""
        today = self.get_today_key()
        
        if today not in self.daily_stats:
            return False
        
        stats = self.daily_stats[today]
        
        # Para se atingiu perda máxima diária
        if stats['total_profit'] <= -self.config.MAX_DAILY_LOSS:
            return True
        
        # Para se atingiu limite de operações
        if stats['trades_count'] >= self.config.MAX_DAILY_TRADES:
            return True
        
        return False
    
    def reset_daily_stats(self):
        """Reseta estatísticas diárias (útil para testes)"""
        today = self.get_today_key()
        if today in self.daily_stats:
            del self.daily_stats[today]
        self.save_daily_stats()