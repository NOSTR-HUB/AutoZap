import logging
from nostr.event import EventKind

# Subscribe to repost events with specific conditions
def subscribe_to_reposts(note_id, clients, payment_handler):
    for client in clients:
        client.subscribe(filters=[{
            "kinds": [EventKind.REPOST],
            "tags": {"e": [note_id]}  # Filter by the target NOTE ID
        }], on_event=lambda event: handle_repost_event(event, payment_handler))

# Handle repost events with comment validation
def handle_repost_event(event, payment_handler):
    # Check if the event has a comment (content is not empty)
    if event.content.strip():
        logging.info(f"Repost with comment detected from {event.pubkey}: {event.content}")
        payment_handler(event.pubkey)
    else:
        logging.info("Repost detected without comment; no payment triggered.")
