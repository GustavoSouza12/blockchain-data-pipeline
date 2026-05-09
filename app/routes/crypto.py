from fastapi import APIRouter
from datetime import datetime, timedelta

from app.database.connection import get_connection


router = APIRouter(
    prefix="/crypto",
    tags=["crypto"]
)


@router.get("/prices")
def get_prices():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT timestamp, asset, price
        FROM crypto_prices
        ORDER BY timestamp DESC
        LIMIT 10
        """
    )

    rows = cursor.fetchall()

    results = []

    for row in rows:

        results.append({
            "timestamp": row[0],
            "asset": row[1],
            "price": row[2]
        })

    conn.close()

    return results