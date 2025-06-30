# import asyncio
# from app.fetcher import run_simulation
# from app.risk import calculate_and_store_risk

# symbols = ["NSE:INFY", "NSE:TCS"]

# async def periodic_risk_task():
#     while True:
#         await asyncio.gather(*(calculate_and_store_risk(sym) for sym in symbols))
#         await asyncio.sleep(10)  # Recalculate every 10 seconds

# if __name__ == "__main__":
#     asyncio.run(asyncio.gather(run_simulation(), periodic_risk_task()))

import asyncio
from app.simulation import simulate_with_risk
from app.api import app
import uvicorn
from app.snowflake_etl import run_simulation
from app.moving_average import monitor_moving_avg
from app.api import create_app
from aiohttp import web

symbol = "NSE:NIFTY 50"

async def start_api():
    app = create_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", 8080)
    await site.start()
    print("aiohttp API running at http://127.0.0.1:8080")

async def main():
    await asyncio.gather(
        run_simulation(symbol),
        start_api()
    )
# async def run_all():
#     await asyncio.gather(
#         #simulate_with_risk("NSE:NIFTY 50", "historical_data/nse_data.csv"),
#         run_simulation(symbol),
#         monitor_moving_avg(symbol),
#         asyncio.to_thread(uvicorn.run, app, host="127.0.0.1", port=8000)
#     )

#http://127.0.0.1:8080/moving_average/NSE:NIFTY 50?window=5

if __name__ == "__main__":
    asyncio.run(main())