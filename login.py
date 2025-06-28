from kiteconnect import KiteConnect
from dotenv import load_dotenv
import os
import sys

load_dotenv(override=True)

def logging_in():
    if sys.argv[1] == "request":
        login_url = kite.login_url()
        print("Login URL:", login_url)
    elif sys.argv[1] == "access":
        request_token = os.getenv("REQUEST_TOKEN")
        print(request_token)
        try:
            data = kite.generate_session(request_token, api_secret=api_secret)
            access_token = data["access_token"]
            print(f"Access Token: {access_token}")
            
            kite.set_access_token(access_token)

            profile = kite.profile()
            print("Your profile details:", profile)

        except Exception as e:
            print(f"Error generating access token: {e}")


api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

kite = KiteConnect(api_key=api_key)

logging_in()

