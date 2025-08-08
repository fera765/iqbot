import logging
from logging.handlers import RotatingFileHandler
from trading_bot.config import LOG_PATH

# Configuração do logger
logger = logging.getLogger("trading_bot")
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

file_handler = RotatingFileHandler(LOG_PATH, maxBytes=1000000, backupCount=3)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

def get_logger():
    return logger