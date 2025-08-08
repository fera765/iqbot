import os
from app.catalog_web import create_app

if __name__ == "__main__":
    email = os.getenv('IQ_EMAIL', '')
    password = os.getenv('IQ_PASSWORD', '')
    assets = os.getenv('ASSETS', 'EURUSD-OTC').split(',')
    assets = [a.strip() for a in assets if a.strip()]
    timeframe = int(os.getenv('TIMEFRAME_SECONDS', '300')) // 60 or 5

    app = create_app(email, password, assets, timeframe)
    host = os.getenv('HOST', '127.0.0.1')
    port = int(os.getenv('PORT', '8000'))
    app.run(host=host, port=port, threaded=True, use_reloader=False)