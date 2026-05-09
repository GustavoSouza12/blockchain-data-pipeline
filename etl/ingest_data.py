import requests
import psycopg2
import time
import os

from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path


# Caminho do .env
env_path = Path(__file__).resolve().parent.parent / ".env"

# Carregar .env
load_dotenv(dotenv_path=env_path)


# DEBUG
print("ENV PATH:", env_path)
print("HOST:", os.getenv("DB_HOST"))
print("PORT:", os.getenv("DB_PORT"))
print("NAME:", os.getenv("DB_NAME"))
print("USER:", os.getenv("DB_USER"))
print("PASSWORD:", os.getenv("DB_PASSWORD"))


# Conexao PostgreSQL
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cursor = conn.cursor()

 
 
# Criar tabela
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS crypto_prices (
        timestamp TEXT,
        asset TEXT,
        price REAL,
        market_cap FLOAT
    )
    """
)

conn.commit()


asset_map = {
    "bitcoin": "BTC",
    "ethereum": "ETH"
}


while True:

    try:

        # API
        url = (
            "https://api.coingecko.com/api/v3/coins/markets"
            "?vs_currency=usd&ids=bitcoin,ethereum"
        )

        response = requests.get(url)

        if response.status_code != 200:

            print("Erro API:", response.status_code)

            time.sleep(30)

            continue

        data = response.json()

        # Timestamp
        timestamp = datetime.utcnow().isoformat()

        # Loop moedas
        for coin in data:

            asset = asset_map.get(
                coin["id"],
                coin["id"].upper()
            )

            price = coin["current_price"]

            market_cap = coin["market_cap"]

            cursor.execute(
                """
                INSERT INTO crypto_prices
                (timestamp, asset, price, market_cap)
                VALUES (%s, %s, %s, %s)
                """,
                (timestamp, asset, price, market_cap)
            )

            print(timestamp, asset, price, market_cap)

        conn.commit()

        print(f"{timestamp} - OK")

        time.sleep(10)

    except Exception as e:

        print("Erro geral:", e)

        time.sleep(30)