import sys

if __name__ == "__main__":
    if "--cli" in sys.argv:
        from trading_bot.cli.main import cli
        cli()
    elif "--web" in sys.argv:
        from trading_bot.web.app import app
        app.run(debug=True, host="0.0.0.0", port=5000)
    else:
        print("Uso: python run.py --cli | --web")