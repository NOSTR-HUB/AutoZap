import logging
import uuid
import time
from nostr.filter import Filter, Filters
from nostr.event import EventKind
from nostr.message_pool import EventMessage
from backend.nostr_bot.transactions import process_payment

def subscribe_to_reposts(note_id, relay_manager):
    # Generate a unique subscription ID
    subscription_id = f"autozap_reposts_{uuid.uuid4().hex}"

    # Define filters for text notes (kind 1) only
    filters = Filters([Filter(kinds=[EventKind.TEXT_NOTE])])

    # Add subscription on all relays
    relay_manager.add_subscription_on_all_relays(subscription_id, filters)
    logging.info("Subscription added to all relays for note ID tracking.")

    # Allow some time for message propagation
    time.sleep(1.25)

    # Continuously check for new events in the message pool
    while True:
        # Retrieve events from the message pool
        while relay_manager.message_pool.has_events():
            event_message = relay_manager.message_pool.get_event()
            event = event_message.event
            handle_repost_event(event, note_id)

        # Sleep briefly to avoid tight-looping
        time.sleep(0.5)

# Handle repost events, paying users for any valid repost, with or without a comment
def handle_repost_event(event, note_id):
    # Access the public key and content directly from the event object
    pubkey = event.public_key
    comment = event.content

    # Check if the event has a tag with "e" that matches the target note_id (indicating a repost)
    if any(tag[1] == note_id for tag in event.tags if tag[0] == "e"):
        logging.info(f"Repost detected from {pubkey}. Comment: {comment}")
        process_payment(pubkey)  # Call process_payment with the pubkey
    else:
        logging.debug("Event does not match repost criteria; ignoring.")
