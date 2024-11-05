import logging
from nostr.client.client import Client
from nostr.key import PrivateKey
from config import NOSTR_PRIVATE_KEY, NOSTR_RELAY_URLS
from .events import subscribe_to_reposts
from .transactions import process_payment

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize private key for signing
private_key = PrivateKey(bytes.fromhex(NOSTR_PRIVATE_KEY))

# Connect to Nostr relays
clients = [Client(url) for url in NOSTR_RELAY_URLS]

def start_bot(note_id):
    logging.info("Starting AutoZap bot...")

    # Initialize relay connections and subscribe to repost events
    for client in clients:
        client.start()
        logging.info(f"Connected to relay {client.relay_url}")

    # Subscribe to reposts of the specific note
    subscribe_to_reposts(note_id, clients, process_payment)

    # Log message indicating bot started successfully
    logging.info("AutoZap bot is monitoring reposts with comments.")
