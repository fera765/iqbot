import sqlite3
from trading_bot.config import DB_PATH

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            pair TEXT,
            direction TEXT,
            result TEXT,
            value REAL,
            profit REAL
        )
    ''')
    conn.commit()
    conn.close()

def insert_trade(timestamp, pair, direction, result, value, profit):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO trades (timestamp, pair, direction, result, value, profit)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (timestamp, pair, direction, result, value, profit))
    conn.commit()
    conn.close()

def get_trades(limit=100):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM trades ORDER BY id DESC LIMIT ?', (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows