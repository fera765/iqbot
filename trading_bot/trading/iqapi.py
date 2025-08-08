from iqoptionapi.stable_api import IQ_Option
import time
from trading_bot.config import IQ_EMAIL, IQ_PASSWORD, USE_DEMO
from trading_bot.utils.logger import get_logger

logger = get_logger()

class IQAPIClient:
    def __init__(self):
        self.api = IQ_Option(IQ_EMAIL, IQ_PASSWORD)
        self.connected = False
        self.connect()

    def connect(self):
        logger.info("Conectando à IQ Option...")
        self.api.connect()
        while True:
            if self.api.check_connect():
                self.connected = True
                logger.info("Conectado com sucesso!")
                if USE_DEMO:
                    self.api.change_balance("PRACTICE")
                break
            else:
                logger.warning("Falha na conexão. Tentando novamente em 5s...")
                time.sleep(5)
                self.api.connect()

    def reconnect(self):
        self.api.close()
        self.connected = False
        self.connect()

    def get_api(self):
        if not self.api.check_connect():
            self.reconnect()
        return self.api