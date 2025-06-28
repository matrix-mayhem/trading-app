from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Numeric, DateTime, func
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

Base = declarative_base()

class MarketData(Base):
    __tablename__ = "market_data"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20))
    price = Column(Numeric)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class RiskMetrics(Base):
    __tablename__ = "risk_metrics"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20))
    ema_5 = Column(Numeric)
    ema_20 = Column(Numeric)
    rsi = Column(Numeric)
    atr = Column(Numeric)
    vwap = Column(Numeric)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

engine = create_async_engine(os.getenv("DB_URL"), echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def insert_price(symbol, price):
    async with SessionLocal() as session:
        new_data = MarketData(symbol=symbol, price=price)
        session.add(new_data)
        await session.commit()

# asyncio.run(init_db())