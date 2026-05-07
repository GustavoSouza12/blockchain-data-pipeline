from fastapi import APIRouter
import psycopg2
from datetime import datetime, timedelta

router = APIRouter(prefix="/crypto", tags=["crypto"])

@router.get("/prices")
def get_prices():

    conn = psycopg2.connect(
    host="localhost",
    database="crypto_db",
    user="postgres",
    password="SUA_SENHA"
    )

    print("Conectado com sucesso!")

    conn.close()
    results = []
    for row in rows:
        result = {
            "timestamp": row[0],
            "asset": row[1],
            "price":row[2]
        }
        results.append(result)


    
    
    

    conn.close()

    return [
        {"timestamp": r[0], "asset": r[1], "price": r[2]}
        for r in rows
    ]

@router.get("/latest")
def get_latest():
    conn = sqlite3.connect("database/database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT t1.timestamp, t1.asset, t1.price, t1.market_cap
        FROM crypto_prices t1
        JOIN (
            SELECT asset, MAX(timestamp) as max_ts
            FROM crypto_prices
            GROUP BY asset
        ) t2
        ON t1.asset = t2.asset AND t1.timestamp = t2.max_ts
    """)

    rows = cursor.fetchall()
    print(rows)
    results = {}

    for row in rows:
        asset = row[1]
        price = row[2]
        market_cap = row[3]

        results[asset] = {
            "price": price,
            "market_cap": market_cap
        }
    
    return results

@router.get('/historical')
def get_historical(asset: str, limit: int = 50):
    conn = sqlite3.connect("database/database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT timestamp, price
        FROM crypto_prices
        WHERE asset = ?
        ORDER BY timestamp DESC
        LIMIT ?
        """,
        (asset.upper(), limit)
    )
    
    rows = cursor.fetchall()

    results = []

    for row in rows:

        ts = row[0]
        price = row[1]

        result = {
            "timestamp": ts,
            "price": price
        }

        results.append(result)

    conn.close()
    return results

@router.get('/summary')
def summary(asset: str, minutes: int = 10):
    limit_time = datetime.utcnow() - timedelta(minutes=minutes)
    limit_time = limit_time.isoformat()
    conn = sqlite3.connect('database/database.db')
    cursor = conn.cursor()
    

    cursor.execute(
        """
        SELECT min(price), max(price), avg(price)
        FROM crypto_prices
        WHERE asset = ?
        AND timestamp >= ?
        """,
        (asset.upper(), limit_time)
    )

    rows = cursor.fetchall()

    row = rows[0]
    if row[0] is None:
        return {"message": "No data for this period"}
    
    min_price = row[0]
    max_price = row[1]
    avg_price = row[2]



    results = {
        "min": min_price,
        "max": max_price,
        "avg": avg_price
    }
    
    conn.close()
    return results 

