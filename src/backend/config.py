import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Variables from .env
LNBITS_API_KEY = os.getenv("LNBITS_API_KEY")
LNBITS_URL = os.getenv("LNBITS_URL")
NOSTR_PRIVATE_KEY = os.getenv("NOSTR_PRIVATE_KEY")
NOSTR_RELAY_URLS = os.getenv("NOSTR_RELAY_URLS").split(",")
PAYMENT_AMOUNT = 1  # Fixed amount of 1 satoshi per qualifying repost
