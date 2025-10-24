"""Main bot module for AutoZap.

This module contains the core bot functionality for monitoring Nostr
events and coordinating payments.
"""

import logging
import time
import signal
import sys
from typing import Optional
from dataclasses import dataclass
from nostr.relay_manager import RelayManager
from backend.config import config
from backend.nostr_bot.events import subscribe_to_reposts, NostrEventError
from backend.db.models import Database

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

@dataclass
class BotStatus:
    """Container for bot status information."""
    
    running: bool = True
    note_id: Optional[str] = None
    relay_manager: Optional[RelayManager] = None

# Global bot status
bot_status = BotStatus()

def signal_handler(signum: int, frame) -> None:
    """Handle shutdown signals gracefully.
    
    Args:
        signum: Signal number
        frame: Current stack frame
    """
    logger.info(f"Received signal {signum}, shutting down...")
    bot_status.running = False

def setup_relays() -> RelayManager:
    """Initialize and connect to Nostr relays.
    
    Returns:
        Configured RelayManager instance
        
    Raises:
        RuntimeError: If relay connection fails
    """
    relay_manager = RelayManager()
    
    for url in config.nostr_relay_urls:
        try:
            relay_manager.add_relay(url)
            logger.info(f"Connected to relay: {url}")
        except Exception as e:
            logger.error(f"Failed to connect to relay {url}: {str(e)}")
    
    if not relay_manager.relays:
        raise RuntimeError("Failed to connect to any relays")
        
    return relay_manager

def run_bot(note_id: str) -> None:
    """Run the main bot loop.
    
    Args:
        note_id: The ID of the note to monitor for reposts
    """
    logger.info(f"Starting AutoZap bot (monitoring note: {note_id[:8]}...)")
    
    # Initialize database
    db = Database(config.db_path)
    logger.info(f"Initialized database at {config.db_path}")
    
    try:
        # Set up relay connections
        bot_status.relay_manager = setup_relays()
        bot_status.note_id = note_id
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Start monitoring reposts
        subscribe_to_reposts(note_id, bot_status.relay_manager)
        
        # Main bot loop
        while bot_status.running:
            try:
                bot_status.relay_manager.run_sync()
                time.sleep(1)  # Prevent CPU thrashing
            except Exception as e:
                logger.error(f"Error in main loop: {str(e)}")
                time.sleep(5)  # Back off on error
                
    except NostrEventError as e:
        logger.error(f"Fatal Nostr event error: {str(e)}")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)
        
    finally:
        if bot_status.relay_manager:
            bot_status.relay_manager.close_connections()
            logger.info("Closed relay connections")

def main() -> None:
    """Main entry point for the bot."""
    # Default note ID to monitor
    note_id = "0987e3bd97d23819c65b50361b17c9a6ba693e2b72665802a12765836301bf94"
    
    try:
        run_bot(note_id)
    except KeyboardInterrupt:
        logger.info("Bot shutdown requested")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
