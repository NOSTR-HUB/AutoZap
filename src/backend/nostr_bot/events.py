"""Nostr event handling for AutoZap.

This module handles subscription to and processing of Nostr events.
"""

import logging
import uuid
import time
from typing import Optional
from dataclasses import dataclass
from nostr.filter import Filter, Filters
from nostr.event import Event, EventKind
from nostr.relay_manager import RelayManager
from nostr.message_pool import EventMessage
from backend.nostr_bot.transactions import process_payment

logger = logging.getLogger(__name__)

@dataclass
class RepostEvent:
    """Container for repost event information."""
    
    pubkey: str
    note_id: str
    comment: str
    event_id: str
    created_at: int

class NostrEventError(Exception):
    """Base exception for Nostr event handling errors."""
    pass

def extract_repost_info(event: Event, target_note_id: str) -> Optional[RepostEvent]:
    """Extract repost information from a Nostr event.
    
    Args:
        event: The Nostr event to analyze
        target_note_id: The ID of the note we're tracking reposts for
        
    Returns:
        RepostEvent if the event is a valid repost, None otherwise
    """
    try:
        # Check if this is a repost of our target note
        is_repost = any(
            tag[0] == "e" and tag[1] == target_note_id 
            for tag in event.tags
        )
        
        if not is_repost:
            return None
            
        return RepostEvent(
            pubkey=event.public_key,
            note_id=target_note_id,
            comment=event.content,
            event_id=event.id,
            created_at=event.created_at
        )
        
    except Exception as e:
        logger.error(f"Error processing event {event.id}: {str(e)}")
        return None

def handle_repost_event(repost: RepostEvent) -> None:
    """Process a repost event and trigger payment if appropriate.
    
    Args:
        repost: The repost event information
    """
    try:
        logger.info(
            f"Processing repost from {repost.pubkey[:8]}... "
            f"of note {repost.note_id[:8]}..."
        )
        
        # Attempt to process payment
        result = process_payment(repost.pubkey, repost.note_id)
        
        if result is None:
            logger.info("Payment skipped due to rate limiting")
        elif result.success:
            logger.info(
                f"Successfully initiated payment to {repost.pubkey[:8]}... "
                f"(BOLT11: {result.bolt11[:30]}...)"
            )
        else:
            logger.error(
                f"Payment failed for {repost.pubkey[:8]}...: "
                f"{result.error_message}"
            )
            
    except Exception as e:
        logger.error(f"Error handling repost event: {str(e)}")

def subscribe_to_reposts(note_id: str, relay_manager: RelayManager) -> None:
    """Subscribe to and monitor repost events for a specific note.
    
    Args:
        note_id: The ID of the note to monitor reposts for
        relay_manager: The Nostr relay manager instance
    """
    subscription_id = f"autozap_reposts_{uuid.uuid4().hex}"
    
    try:
        # Set up filters for text notes
        filters = Filters([
            Filter(kinds=[EventKind.TEXT_NOTE])
        ])
        
        # Subscribe to events
        relay_manager.add_subscription_on_all_relays(subscription_id, filters)
        logger.info(
            f"Monitoring reposts of note {note_id[:8]}... "
            f"(Subscription: {subscription_id})"
        )
        
        # Allow time for subscription setup
        time.sleep(1.25)
        
        # Event monitoring loop
        while True:
            try:
                # Process events from the message pool
                while relay_manager.message_pool.has_events():
                    event_msg: EventMessage = relay_manager.message_pool.get_event()
                    
                    if repost := extract_repost_info(event_msg.event, note_id):
                        handle_repost_event(repost)
                        
                # Brief sleep to prevent CPU thrashing
                time.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Error in event processing loop: {str(e)}")
                time.sleep(1)  # Back off on error
                
    except Exception as e:
        logger.error(f"Fatal error in repost subscription: {str(e)}")
        raise NostrEventError(f"Failed to monitor reposts: {str(e)}") from e
