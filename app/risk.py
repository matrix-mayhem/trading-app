import pandas as pd
import pandas_ta as ta
from db import SessionLocal, MarketData, RiskMetrics
from sqlalchemy import select

async def calculate_and_store_risk(symbol):
    async with SessionLocal() as session:
        result = await session.execute(
            select(MarketData).where(MarketData.symbol == symbol).order_by(MarketData.timestamp.desc()).limit(100)
        )
        rows = result.scalars().all()

    if not rows:
        print(f"No price data found for {symbol}")
        return

    data = pd.DataFrame([{"price": float(row.price), "timestamp": row.timestamp} for row in rows])
    data.sort_values("timestamp", inplace=True)

    data['EMA_5'] = ta.ema(data['price'], length=5)
    data['EMA_20'] = ta.ema(data['price'], length=20)
    data['RSI'] = ta.rsi(data['price'], length=14)
    data['ATR'] = ta.atr(high=data['price'], low=data['price'], close=data['price'], length=14)
    data['VWAP'] = data['price'].expanding().mean()

    latest = data.iloc[-1]

    async with SessionLocal() as session:
        metrics = RiskMetrics(
            symbol=symbol,
            ema_5=latest['EMA_5'],
            ema_20=latest['EMA_20'],
            rsi=latest['RSI'],
            atr=latest['ATR'],
            vwap=latest['VWAP']
        )
        session.add(metrics)
        await session.commit()
