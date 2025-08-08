import click
import threading
import time
from trading_bot.trading.iqapi import IQAPIClient
from trading_bot.trading.manager import TradingManager
from trading_bot.config import *
from trading_bot.utils.logger import get_logger

logger = get_logger()

@click.group()
def cli():
    pass

@click.command()
def start():
    "Inicia o robô de trading."
    api_client = IQAPIClient()
    manager = TradingManager(api_client.get_api())
    t = threading.Thread(target=manager.start)
    t.start()
    try:
        while manager.running:
            click.clear()
            click.echo("\n--- Estatísticas em tempo real ---")
            for pair, stats in manager.stats.items():
                click.echo(f"{pair}: {stats}")
            click.echo("\nComandos: [p]ausar, [s]air")
            if click.getchar() == 'p':
                manager.stop()
            elif click.getchar() == 's':
                manager.stop()
                break
            time.sleep(2)
    except KeyboardInterrupt:
        manager.stop()

@click.command()
def config():
    "Exibe e permite alterar parâmetros de operação."
    click.echo(f"Pares atuais: {PAIR_LIST}")
    click.echo(f"Valor entrada: {ENTRY_VALUE}")
    click.echo(f"Martingale: {MARTINGALE}")
    click.echo(f"Ciclos MHI: {MHI_CYCLES}")
    click.echo(f"Stop win: {STOP_WIN}")
    click.echo(f"Stop loss: {STOP_LOSS}")
    click.echo(f"Limite trades: {MAX_TRADES}")
    click.echo("Edite o arquivo config.py para alterar parâmetros.")

cli.add_command(start)
cli.add_command(config)

if __name__ == "__main__":
    cli()