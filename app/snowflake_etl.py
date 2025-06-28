import snowflake.connector
from dotenv import load_dotenv
import os
from db import SessionLocal, MarketData
from sqlalchemy import select

# Load environment variables for Snowflake configuration directly in this module
load_dotenv(override=True)

def snowflake_conn():
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA")
    )

async def export_price_data(symbol):
    async with SessionLocal() as session:
        result = await session.execute(
            select(MarketData).where(MarketData.symbol == symbol).order_by(MarketData.timestamp.desc()).limit(50)
        )
        rows = result.scalars().all()

    if not rows:
        print(f"No data for {symbol}")
        return

    conn = snowflake_conn()
    cs = conn.cursor()

    try:
        table_name = symbol.replace(":", "_").replace(" ", "_")

        cs.execute(f"""CREATE TABLE IF NOT EXISTS market_data_{table_name} (
            price FLOAT,
            timestamp TIMESTAMP
        )""")

        for row in rows:
            cs.execute(f"""INSERT INTO market_data_{table_name} (price, timestamp)
                                 VALUES (%s, %s)""", (row.price, row.timestamp))

        print(f"Uploaded {len(rows)} rows to Snowflake for {symbol}")

    finally:
        cs.close()
        conn.close()
