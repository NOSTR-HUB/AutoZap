import os
from dotenv import load_dotenv

load_dotenv()

# Settings for API keys, URLs, and other configurations
LNBITS_API_KEY = os.getenv("LNBITS_API_KEY")
LNBITS_URL = os.getenv("LNBITS_URL")
NOSTR_PRIVATE_KEY = os.getenv("NOSTR_PRIVATE_KEY")
NOSTR_RELAY_URLS = os.getenv("NOSTR_RELAY_URLS").split(",")
PAYMENT_AMOUNT = 1  # Satoshi amount for each qualifying repost
