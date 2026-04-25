import requests
import sqlite3
from datetime import datetime

# API (preço BTC e ETH)
url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"

response = requests.get(url)
data = response.json()

# Tratamento
timestamp = datetime.utcnow()
btc_price = data["bitcoin"]["usd"]
eth_price = data["ethereum"]["usd"]

# Banco
conn = sqlite3.connect("database/database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS crypto_prices (
    timestamp TEXT,
    asset TEXT,
    price REAL
)
""")

cursor.execute("INSERT INTO crypto_prices VALUES (?, ?, ?)", (timestamp, "BTC", btc_price))
cursor.execute("INSERT INTO crypto_prices VALUES (?, ?, ?)", (timestamp, "ETH", eth_price))

conn.commit()
conn.close()

print("OK: dados inseridos")