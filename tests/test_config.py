"""Test configuration validation."""

import os
import pytest
from src.backend.config import validate_config, Config

@pytest.fixture
def mock_env(monkeypatch):
    """Set up test environment variables."""
    env_vars = {
        "LNBITS_API_KEY": "test_key",
        "LNBITS_URL": "https://test.lnbits.com",
        "NOSTR_RELAY_URLS": "wss://relay1.com,wss://relay2.com",
        "PAYMENT_AMOUNT": "1000",
        "RATE_LIMIT_HOURS": "24",
        "DB_PATH": "test.db"
    }
    
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
    return env_vars

def test_valid_config(mock_env):
    """Test configuration validation with valid inputs."""
    config = validate_config()
    assert isinstance(config, Config)
    assert config.lnbits_api_key == mock_env["LNBITS_API_KEY"]
    assert config.lnbits_url == mock_env["LNBITS_URL"]
    assert len(config.nostr_relay_urls) == 2
    assert config.payment_amount == 1000
    assert config.rate_limit_hours == 24
    assert config.db_path == "test.db"

def test_missing_required_config(monkeypatch):
    """Test configuration validation with missing required values."""
    # Clear environment variables
    for key in ["LNBITS_API_KEY", "LNBITS_URL", "NOSTR_RELAY_URLS"]:
        monkeypatch.delenv(key, raising=False)
    
    with pytest.raises(ValueError):
        validate_config()

def test_invalid_payment_amount(monkeypatch):
    """Test configuration validation with invalid payment amount."""
    env_vars = {
        "LNBITS_API_KEY": "test_key",
        "LNBITS_URL": "https://test.lnbits.com",
        "NOSTR_RELAY_URLS": "wss://relay1.com",
        "PAYMENT_AMOUNT": "0"
    }
    
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
    
    with pytest.raises(ValueError, match="PAYMENT_AMOUNT must be at least 1 satoshi"):
        validate_config()

def test_invalid_urls(monkeypatch):
    """Test configuration validation with invalid URLs."""
    # Test invalid LNbits URL
    env_vars = {
        "LNBITS_API_KEY": "test_key",
        "LNBITS_URL": "invalid_url",
        "NOSTR_RELAY_URLS": "wss://relay1.com"
    }
    
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
    
    with pytest.raises(ValueError, match="Invalid LNbits URL"):
        validate_config()
    
    # Test invalid relay URL
    env_vars["LNBITS_URL"] = "https://test.lnbits.com"
    env_vars["NOSTR_RELAY_URLS"] = "invalid_relay_url"
    
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
    
    with pytest.raises(ValueError, match="Invalid relay URL"):
        validate_config()