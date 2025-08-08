import logging
import os
from datetime import datetime
from colorama import Fore, Style, init

# Inicializa colorama para cores no terminal
init()

class ColoredFormatter(logging.Formatter):
    """Formatter personalizado com cores"""
    
    COLORS = {
        'DEBUG': Fore.BLUE,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT
    }
    
    def format(self, record):
        # Adiciona cor ao nível do log
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{Style.RESET_ALL}"
        
        # Adiciona cor ao timestamp
        record.asctime = f"{Fore.CYAN}{record.asctime}{Style.RESET_ALL}"
        
        return super().format(record)

class TradingLogger:
    """Logger personalizado para o robô de trading"""
    
    def __init__(self, config):
        self.config = config
        self.logger = self.setup_logger()
    
    def setup_logger(self):
        """Configura o logger"""
        logger = logging.getLogger('TradingBot')
        logger.setLevel(getattr(logging, self.config.LOG_LEVEL))
        
        # Remove handlers existentes
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # Handler para console com cores
        console_handler = logging.StreamHandler()
        console_formatter = ColoredFormatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # Handler para arquivo
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        file_handler = logging.FileHandler(
            f'logs/trading_{datetime.now().strftime("%Y%m%d")}.log',
            encoding='utf-8'
        )
        file_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        return logger
    
    def info(self, message):
        """Log de informação"""
        self.logger.info(message)
    
    def warning(self, message):
        """Log de aviso"""
        self.logger.warning(message)
    
    def error(self, message):
        """Log de erro"""
        self.logger.error(message)
    
    def debug(self, message):
        """Log de debug"""
        self.logger.debug(message)
    
    def critical(self, message):
        """Log crítico"""
        self.logger.critical(message)
    
    def log_trade(self, trade_data):
        """Log específico para operações"""
        action = trade_data.get('action', 'UNKNOWN')
        asset = trade_data.get('asset', 'UNKNOWN')
        amount = trade_data.get('amount', 0)
        profit = trade_data.get('profit', 0)
        
        if profit > 0:
            profit_color = Fore.GREEN
            result = "WIN"
        elif profit < 0:
            profit_color = Fore.RED
            result = "LOSS"
        else:
            profit_color = Fore.YELLOW
            result = "DRAW"
        
        message = f"TRADE: {action.upper()} {asset} | Amount: ${amount} | Profit: {profit_color}${profit:.2f}{Style.RESET_ALL} | Result: {result}"
        self.info(message)
    
    def log_signal(self, signal, asset, strategy_name):
        """Log específico para sinais"""
        if signal == 'call':
            signal_color = Fore.GREEN
        elif signal == 'put':
            signal_color = Fore.RED
        else:
            signal_color = Fore.YELLOW
        
        message = f"SIGNAL: {signal_color}{signal.upper()}{Style.RESET_ALL} on {asset} | Strategy: {strategy_name}"
        self.info(message)
    
    def log_connection(self, status):
        """Log de status de conexão"""
        if status:
            message = f"{Fore.GREEN}Connected to IQ Option{Style.RESET_ALL}"
        else:
            message = f"{Fore.RED}Failed to connect to IQ Option{Style.RESET_ALL}"
        self.info(message)
    
    def log_balance(self, balance):
        """Log de saldo"""
        message = f"Balance: {Fore.CYAN}${balance:.2f}{Style.RESET_ALL}"
        self.info(message)
    
    def log_stats(self, stats):
        """Log de estatísticas"""
        message = f"Daily Stats - Trades: {stats['trades_count']} | Profit: ${stats['total_profit']:.2f} | Wins: {stats['wins']} | Losses: {stats['losses']}"
        self.info(message)