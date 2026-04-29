import requests
import sqlite3
from datetime import datetime
import time

# Banco
conn = sqlite3.connect("database/database.db")  
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS crypto_prices (
    timestamp text,
    asset TEXT,
    price REAL,
    market_cap FLOAT
)
""")

while True:
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin,ethereum"

        response = requests.get(url)

        if response.status_code != 200:
            print("Erro API:", response.status_code)
            time.sleep(30)
            continue

        data = response.json()

        timestamp = datetime.utcnow().isoformat()

        conn = sqlite3.connect("database/database.db")  
        cursor = conn.cursor()

        asset_map = {
            "bitcoin": "BTC",
            "ethereum": "ETH"
        }

        for coin in data:
            asset = asset_map.get(coin["id"], coin["id"].upper())
            price = coin["current_price"]
            market_cap = coin["market_cap"]

            cursor.execute(
                """
                INSERT INTO crypto_prices (timestamp, asset, price, market_cap)
                VALUES (?,?,?,?)
                """,
                (timestamp, asset, price, market_cap)
            )

            print(timestamp, asset, price, market_cap)

        conn.commit()
        conn.close()

        print(f"{timestamp} - OK")

        time.sleep(10)

    except Exception as e:
        print("Erro geral:", e)
        time.sleep(30)
