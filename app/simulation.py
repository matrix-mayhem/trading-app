import pandas as pd
import asyncio
from app.db import SessionLocal, MarketData
from app.risk import calculate_and_store_risk

async def simulate_with_risk(symbol, csv_path):
    df = pd.read_csv(csv_path)
    
    for _, row in df.iterrows():
        async with SessionLocal() as session:
            price = MarketData(
                symbol=symbol,
                price=float(row['price']),
                timestamp=row['timestamp']
            )
            session.add(price)
            await session.commit()

        await calculate_and_store_risk(symbol)
        print(f"Inserted price {row['price']} & updated risk for {symbol}")
        await asyncio.sleep(1)