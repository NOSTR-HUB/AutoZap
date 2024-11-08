import logging
import time
from nostr.relay_manager import RelayManager
from backend.config import NOSTR_RELAY_URLS
from src.backend.nostr_bot.events import subscribe_to_reposts
from src.backend.nostr_bot.transactions import process_payment

# Configure logging
logging.basicConfig(level=logging.INFO)

def start_bot(note_id):
    logging.info("Starting AutoZap bot...")

    # Initialize RelayManager and add relays
    relay_manager = RelayManager()
    for url in NOSTR_RELAY_URLS:
        relay_manager.add_relay(url)
        logging.info(f"Connected to relay {url}")

    # Call subscribe_to_reposts to monitor reposts of the specified note
    subscribe_to_reposts(note_id, relay_manager)

    # Keep running and listening to events
    try:
        while True:
            relay_manager.run_sync()  # Sync with the relay for incoming events
            time.sleep(1)  # Avoid maxing out CPU
    except KeyboardInterrupt:
        logging.info("AutoZap bot stopped.")
    finally:
        relay_manager.close_connections()

# Main entry point
if __name__ == "__main__":
    # Set the specific NOTE ID to track
    note_id = "0987e3bd97d23819c65b50361b17c9a6ba693e2b72665802a12765836301bf94"
    start_bot(note_id)
