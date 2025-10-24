"""Configuration management for AutoZap.

This module handles loading and validating configuration from environment variables
and provides a centralized configuration object for the application.
"""

import os
import logging
from dataclasses import dataclass
from typing import List
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

@dataclass
class Config:
    """Configuration container for AutoZap."""
    
    lnbits_api_key: str
    lnbits_url: str
    nostr_relay_urls: List[str]
    payment_amount: int
    rate_limit_hours: int
    db_path: str

def validate_config() -> Config:
    """Load and validate configuration from environment variables.
    
    Returns:
        Config object containing validated configuration values
        
    Raises:
        ValueError: If any required configuration values are missing or invalid
    """
    load_dotenv()
    
    # Required environment variables
    lnbits_api_key = os.getenv("LNBITS_API_KEY")
    lnbits_url = os.getenv("LNBITS_URL")
    relay_urls = os.getenv("NOSTR_RELAY_URLS")
    
    # Optional environment variables with defaults
    payment_amount = int(os.getenv("PAYMENT_AMOUNT", "1"))
    rate_limit_hours = int(os.getenv("RATE_LIMIT_HOURS", "24"))
    db_path = os.getenv("DB_PATH", "payments.db")
    
    # Validation
    if not lnbits_api_key:
        raise ValueError("LNBITS_API_KEY environment variable is required")
        
    if not lnbits_url:
        raise ValueError("LNBITS_URL environment variable is required")
        
    if not relay_urls:
        raise ValueError("NOSTR_RELAY_URLS environment variable is required")
        
    if payment_amount < 1:
        raise ValueError("PAYMENT_AMOUNT must be at least 1 satoshi")
        
    if rate_limit_hours < 1:
        raise ValueError("RATE_LIMIT_HOURS must be at least 1")
    
    # Parse relay URLs
    relay_url_list = [url.strip() for url in relay_urls.split(",") if url.strip()]
    if not relay_url_list:
        raise ValueError("At least one valid relay URL must be provided")
    
    # Validate URLs
    for url in relay_url_list:
        if not url.startswith(("ws://", "wss://")):
            raise ValueError(f"Invalid relay URL: {url}. Must start with ws:// or wss://")
            
    if not lnbits_url.startswith(("http://", "https://")):
        raise ValueError(f"Invalid LNbits URL: {lnbits_url}. Must start with http:// or https://")
    
    return Config(
        lnbits_api_key=lnbits_api_key,
        lnbits_url=lnbits_url,
        nostr_relay_urls=relay_url_list,
        payment_amount=payment_amount,
        rate_limit_hours=rate_limit_hours,
        db_path=db_path
    )

# Initialize configuration
config = validate_config()
