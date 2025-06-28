from kiteconnect import KiteConnect
from dotenv import load_dotenv
import os
import sys
#from .login import kite
load_dotenv(override=True)

api_key = os.getenv("API_KEY")
kite = KiteConnect(api_key=api_key)
kite.set_access_token(os.getenv("ACCESS_TOKEN"))

# profile = kite.profile()
# print(profile)
print("Fetching holdings...")
try:
    holdings = kite.holdings()
    for item in holdings:
        print(f"  {item['tradingsymbol']}: Quantity={item['quantity']}, Average Price={item['average_price']}")
except Exception as e:
    print(f"Error fetching holdings: {e}")

