from app.snowflake_etl import snowflake_conn
import os
import asyncio

async def fetch_moving_average(symbol, window=5):
    conn = snowflake_conn()
    cursor = conn.cursor()

    query = f"""
    WITH ordered_data AS (
        SELECT symbol, price, timestamp,
               ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY timestamp) AS row_num
        FROM market_data
        WHERE symbol = %s
    )
    SELECT symbol, price, timestamp,
           AVG(price) OVER (ORDER BY row_num ROWS {window-1} PRECEDING) AS moving_avg
    FROM ordered_data
    WHERE symbol = %s
    ORDER BY timestamp DESC
    LIMIT 1;
    """

    cursor.execute(query, (symbol, symbol))
    rows = cursor.fetchall()

    # print("\nLatest Moving Averages:")
    # for row in rows:
    #     print(row)

    cursor.close()
    conn.close()

    return [
        {"symbol": r[0], "price": float(r[1]), "timestamp": str(r[2]), "moving_avg": float(r[3])}
        for r in rows
    ]

async def monitor_moving_avg(symbol, interval=5):
    while True:
        await fetch_moving_average(symbol)
        await asyncio.sleep(interval)

    # cursor.execute(query, (symbol, symbol))
    # for row in cursor.fetchall():
    #     print(row)

    # cursor.close()
    # conn.close()
