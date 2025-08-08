import threading
from trading_bot.trading.mhi import MHI
from trading_bot.config import PAIR_LIST, ENTRY_VALUE, MARTINGALE, MHI_CYCLES, STOP_WIN, STOP_LOSS, MAX_TRADES
from trading_bot.utils.logger import get_logger
from trading_bot.utils.db import init_db

logger = get_logger()

class TradingManager:
    def __init__(self, api):
        self.api = api
        self.pairs = PAIR_LIST.copy()
        self.entry_value = ENTRY_VALUE
        self.martingale = MARTINGALE
        self.cycles = MHI_CYCLES
        self.stop_win = STOP_WIN
        self.stop_loss = STOP_LOSS
        self.max_trades = MAX_TRADES
        self.running = False
        self.threads = []
        self.stats = {p: {"wins":0, "losses":0, "trades":0, "profit":0.0} for p in self.pairs}
        init_db()

    def start(self):
        self.running = True
        for pair in self.pairs:
            t = threading.Thread(target=self.run_pair, args=(pair,))
            t.start()
            self.threads.append(t)
        logger.info("Robô iniciado para pares: %s", self.pairs)

    def stop(self):
        self.running = False
        logger.info("Robô pausado/parado.")

    def run_pair(self, pair):
        mhi = MHI(self.api, pair, self.entry_value, self.martingale, self.cycles)
        while self.running:
            mhi.run_cycle()
            self.stats[pair] = mhi.stats.copy()
            if mhi.stats["profit"] >= self.stop_win:
                logger.info(f"Stop win atingido para {pair}!")
                break
            if abs(mhi.stats["profit"]) >= self.stop_loss:
                logger.info(f"Stop loss atingido para {pair}!")
                break
            if mhi.stats["trades"] >= self.max_trades:
                logger.info(f"Limite diário de trades atingido para {pair}!")
                break