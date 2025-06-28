from fastapi import FastAPI, HTTPException
from risk import calculate_and_store_risk
from db import SessionLocal, RiskMetrics
from sqlalchemy import select
from db import MarketData
from snowflake_etl import export_price_data

app = FastAPI()

@app.get("/price/{symbol}")
async def get_latest_price(symbol: str):
    async with SessionLocal() as session:
        result = await session.execute(
            select(MarketData).where(MarketData.symbol == symbol).order_by(MarketData.timestamp.desc()).limit(1)
        )
        latest = result.scalars().first()

    if not latest:
        raise HTTPException(status_code=404, detail="No price data found")

    return {
        "symbol": latest.symbol,
        "price": float(latest.price),
        "timestamp": latest.timestamp
    }


@app.post("/upload/{symbol}")
async def upload_to_snowflake(symbol: str):
    try:
        await export_price_data(symbol)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Snowflake upload failed: {str(e)}")

    return {"message": f"Data for {symbol} uploaded to Snowflake successfully"}

@app.get("/risk/{symbol}")
async def get_risk_metrics(symbol: str):
    await calculate_and_store_risk(symbol)
    
    async with SessionLocal() as session:
        result = await session.execute(
            select(RiskMetrics).where(RiskMetrics.symbol == symbol).order_by(RiskMetrics.timestamp.desc()).limit(1)
        )
        latest = result.scalars().first()

    if latest:
        return {
            "symbol": symbol,
            "ema_5": latest.ema_5,
            "ema_20": latest.ema_20,
            "rsi": latest.rsi,
            "atr": latest.atr,
            "vwap": latest.vwap,
            "timestamp": latest.timestamp
        }
    return {"message": "No risk metrics found"}
