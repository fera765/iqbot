import numpy as np
import pandas as pd
import time
from trading_bot.utils.logger import get_logger
from trading_bot.utils.db import insert_trade

logger = get_logger()

class MHI:
    def __init__(self, api, pair, entry_value, martingale, cycles):
        self.api = api
        self.pair = pair
        self.entry_value = entry_value
        self.martingale = martingale
        self.cycles = cycles
        self.stats = {"wins": 0, "losses": 0, "trades": 0, "profit": 0.0}

    def get_last_candles(self, n=3):
        # IQ Option espera o par em maiúsculo e o tempo em segundos
        candles = self.api.get_candles(self.pair, 60, n+1, time.time())
        # Remove a última vela (ainda em formação)
        candles = candles[:-1]
        return candles

    def analyze_pattern(self):
        # Estratégia MHI: pega as 3 últimas velas M1, ignora doji
        candles = self.get_last_candles(3)
        colors = []
        for c in candles:
            if c['close'] > c['open']:
                colors.append('g')  # green
            elif c['close'] < c['open']:
                colors.append('r')  # red
            else:
                colors.append('d')  # doji
        # Se houver doji, não opera
        if 'd' in colors:
            logger.info(f"Doji detectado em {self.pair}, pulando ciclo.")
            return None
        # Se maioria for verde, entra vendido (put); se maioria vermelha, entra comprado (call)
        if colors.count('g') > colors.count('r'):
            return 'put'
        elif colors.count('r') > colors.count('g'):
            return 'call'
        else:
            return None

    def execute_trade(self, direction, value):
        logger.info(f"Operando {self.pair} {direction} valor {value}")
        # Executa ordem binária para expiração de 1 minuto
        check, order_id = self.api.buy(value, self.pair, direction, 1)
        if not check:
            logger.error(f"Falha ao enviar ordem para {self.pair}")
            return 'error', 0.0
        # Aguarda expiração e resultado
        while True:
            result = self.api.check_win_v3(order_id)
            if isinstance(result, tuple):
                win, profit = result
                break
            time.sleep(1)
        if win:
            status = 'win' if profit > 0 else 'loss'
        else:
            status = 'loss'
        insert_trade(time.strftime('%Y-%m-%d %H:%M:%S'), self.pair, direction, status, value, profit)
        self.stats["trades"] += 1
        if status == 'win':
            self.stats["wins"] += 1
            self.stats["profit"] += profit
        else:
            self.stats["losses"] += 1
            self.stats["profit"] += profit
        return status, profit

    def run_cycle(self):
        for _ in range(self.cycles):
            # Espera o início do próximo ciclo MHI (minuto múltiplo de 5)
            now = time.localtime()
            wait = 60 - now.tm_sec
            logger.info(f"Aguardando {wait}s para sincronizar ciclo MHI...")
            time.sleep(wait)
            minute = time.localtime().tm_min
            if minute % 5 == 0:
                direction = self.analyze_pattern()
                if direction:
                    value = self.entry_value
                    for mg in range(2 if self.martingale else 1):
                        result, profit = self.execute_trade(direction, value)
                        if result == 'win':
                            break
                        elif result == 'error':
                            break
                        else:
                            value *= 2  # Martingale
                else:
                    logger.info(f"Sem operação neste ciclo para {self.pair}.")
            else:
                logger.info(f"Fora do ciclo MHI, aguardando próximo...")
            time.sleep(60)  # Espera para próximo ciclo