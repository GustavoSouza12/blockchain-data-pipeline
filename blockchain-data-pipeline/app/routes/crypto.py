from fastapi import APIRouter
import sqlite3

router = APIRouter(prefix="/crypto", tags=["crypto"])

@router.get("/prices")
def get_prices():
    conn = sqlite3.connect("database/database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT timestamp, asset, price
        FROM crypto_prices
        ORDER BY timestamp DESC
        GROUP BY asset, MAX(timestamp)
        LIMIT 10
    """)

    rows = cursor.fetchall()
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