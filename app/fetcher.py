from kiteconnect import KiteConnect
from dotenv import load_dotenv
import asyncio
import os
import sys
import datetime
from db import init_db, insert_price
from login import kite

load_dotenv(override=True)

access_token = os.getenv("ACCESS_TOKEN")
kite.set_access_token(access_token)

live_symbols = ["NSE:NIFTY 50", "NSE:TCS", "NSE:RELIANCE"]
hist_symbols = {"NSE:NIFTY 50": 256265, "NSE:TCS": 2953217}

async def fetch_price(symbol):
    try:
        price_data = kite.ltp(symbol)
        price = price_data[symbol]["last_price"]
        #await insert_price(symbol, price)
        print(f"{symbol} Price: {price}")
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")

async def replay_historical(symbol: str, token: str):
    from_date = datetime.datetime(2024, 6, 25, 9, 15)
    to_date = datetime.datetime(2024, 6, 25, 15, 30)

    data = kite.historical_data(token, from_date, to_date, interval="5minute")

    for candle in data:
        price = candle['close']
        #await insert_price(symbol, price)
        print(f"[Simulated] {symbol} Price: {price} at {candle['date']}")
        await asyncio.sleep(0.5)

async def run_fetch_loop():
    print("Initializing database...")
    try:
        await init_db()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"ERROR: Failed to initialize database: {e}")
        return
    
    print("Starting price fetch loop...")
    while True:
        tasks = [fetch_price(sym) for sym in live_symbols]
        await asyncio.gather(*tasks)
        print("--- All symbols fetched. Waiting for next interval. ---")
        await asyncio.sleep(0.2)

async def run_simulation():
    tasks = [replay_historical(sym, token) for sym, token in hist_symbols.items()]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        if sys.argv[1] == "live":
            asyncio.run(run_fetch_loop())
        elif sys.argv[1] == "backtest":
            asyncio.run(run_simulation())
    except IndexError:
        print("Usage: python fetcher.py [live|backtest]")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nProcess stopped by user.")
    except Exception as e:
        print(f"An unexpected error occurred in the main loop: {e}")