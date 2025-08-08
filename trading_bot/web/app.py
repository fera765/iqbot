from flask import Flask, render_template, request, redirect, url_for
from trading_bot.utils.db import get_trades
from trading_bot.config import *
from trading_bot.trading.iqapi import IQAPIClient
from trading_bot.trading.manager import TradingManager
import threading

app = Flask(__name__)
manager = None
api_client = None

@app.route("/")
def dashboard():
    trades = get_trades(50)
    stats = manager.stats if manager else {}
    return render_template("dashboard.html", trades=trades, stats=stats, config={
        "PAIR_LIST": PAIR_LIST, "ENTRY_VALUE": ENTRY_VALUE, "MARTINGALE": MARTINGALE,
        "MHI_CYCLES": MHI_CYCLES, "STOP_WIN": STOP_WIN, "STOP_LOSS": STOP_LOSS, "MAX_TRADES": MAX_TRADES
    })

@app.route("/start")
def start():
    global manager, api_client
    if not manager or not manager.running:
        api_client = IQAPIClient()
        manager = TradingManager(api_client.get_api())
        t = threading.Thread(target=manager.start)
        t.start()
    return redirect(url_for('dashboard'))

@app.route("/stop")
def stop():
    global manager
    if manager:
        manager.stop()
    return redirect(url_for('dashboard'))

@app.route("/config", methods=["POST"])
def update_config():
    # Para simplificação, instruir usuário a editar config.py
    return "Edite o arquivo config.py e reinicie o robô para aplicar alterações.", 200