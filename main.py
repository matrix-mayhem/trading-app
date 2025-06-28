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

async def run_all():
    await asyncio.gather(
        simulate_with_risk("NSE:INFY", "historical_data/infy_data.csv"),
        asyncio.to_thread(uvicorn.run, app, host="127.0.0.1", port=8000)
    )

if __name__ == "__main__":
    asyncio.run(run_all())