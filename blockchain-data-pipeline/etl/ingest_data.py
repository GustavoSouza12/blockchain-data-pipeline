import requests
import sqlite3
from datetime import datetime


# API (preço BTC e ETH)
url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin,ethereum"

response = requests.get(url)
data = response.json()

# Tratamento
timestamp = datetime.utcnow().isoformat()


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

records = []


asset_map = {
    "bitcoin": "BTC",
    "ethereum": "ETH"
}

for coin in data:
    asset = asset_map.get(coin["id"], coin["id"].upper())
    price = coin["current_price"]
    market_cap = coin["market_cap"]

    record = {
        "timestamp": timestamp,
        "asset": asset,
        "price": price,
        "market_cap": market_cap
    }
    print(timestamp, asset, price, market_cap)
    records.append(record)

    cursor.execute(
        """
        INSERT INTO crypto_prices (timestamp, asset, price, market_cap)
        VALUES (?,?,?,?)
        """,
        (timestamp, asset, price, market_cap)
    )
conn.commit()

conn.close()

print("OK: dados inseridos")
