import pandas as pd
from kiteconnect import KiteConnect
from dotenv import load_dotenv
import os
import sys

load_dotenv(override=True)

api_key = os.getenv("API_KEY")
access_token = os.getenv("ACCESS_TOKEN")
kite = KiteConnect(api_key=api_key)
kite.set_access_token(access_token)


def get_instrument_token_from_master(tradingsymbol, exchange="NSE"):
    """
    Downloads the full instrument list and finds the token for a given symbol.
    It's recommended to download the instruments list once a day and store it.
    """
    print(f"Downloading all instruments for {exchange}...")
    try:
        # Get all instruments for a specific exchange (e.g., NSE)
        # You can also use kite.instruments() without arguments to get all exchanges
        instrument_list = kite.instruments(exchange=exchange)
        df = pd.DataFrame(instrument_list)

        # Filter for the specific trading symbol
        filtered_df = df[(df['tradingsymbol'] == tradingsymbol) & (df['exchange'] == exchange)]

        if not filtered_df.empty:
            instrument_token = filtered_df.iloc[0]['instrument_token']
            print(f"Found instrument token for {exchange}:{tradingsymbol}: {instrument_token}")
            return instrument_token
        else:
            print(f"Instrument token not found for {exchange}:{tradingsymbol}")
            return None
    except Exception as e:
        print(f"Error fetching instrument list or token: {e}")
        return None

# --- Example Usage ---
if __name__ == "__main__":
    nifty_token = get_instrument_token_from_master("NIFTY 50", "NSE")
    tcs_token = get_instrument_token_from_master("TCS", "NSE")
    reliance_token = get_instrument_token_from_master("RELIANCE", "NSE")

    # Now you can use these tokens
    if nifty_token:
        print(f"INFY Token: {nifty_token}")
    if tcs_token:
        print(f"TCS Token: {tcs_token}")
    if reliance_token:
        print(f"RELIANCE Token: {reliance_token}")

    # You would then use these tokens in your symbols dictionary for your price fetching loop
    # symbols = {"NSE:INFY": infy_token, "NSE:TCS": tcs_token, "NSE:RELIANCE": reliance_token}