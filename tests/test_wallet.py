"""Test Lightning Network payment operations."""

import pytest
import responses
from backend.ln_wallet.wallet import create_invoice, InvoiceGenerationError

@pytest.fixture
def mock_config(monkeypatch):
    """Set up test configuration."""
    env_vars = {
        "LNBITS_API_KEY": "test_key",
        "LNBITS_URL": "https://test.lnbits.com",
        "PAYMENT_AMOUNT": "1000"
    }
    
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)

@responses.activate
def test_create_invoice_success(mock_config):
    """Test successful invoice creation."""
    # Mock LNbits API response
    responses.add(
        responses.POST,
        "https://test.lnbits.com/api/v1/payments",
        json={
            "payment_request": "test_bolt11",
            "payment_hash": "test_hash"
        },
        status=201
    )
    
    result = create_invoice("test_npub", "test_note")
    assert result.success
    assert result.status == "invoice_generated"
    assert result.bolt11 == "test_bolt11"
    assert result.payment_hash == "test_hash"

@responses.activate
def test_create_invoice_failure(mock_config):
    """Test invoice creation failure."""
    # Mock LNbits API error response
    responses.add(
        responses.POST,
        "https://test.lnbits.com/api/v1/payments",
        json={"error": "Failed to generate invoice"},
        status=400
    )
    
    with pytest.raises(InvoiceGenerationError):
        create_invoice("test_npub", "test_note")

@responses.activate
def test_create_invoice_network_error(mock_config):
    """Test invoice creation with network error."""
    # Mock network timeout
    responses.add(
        responses.POST,
        "https://test.lnbits.com/api/v1/payments",
        body=responses.ConnectionError("Connection timeout")
    )
    
    with pytest.raises(InvoiceGenerationError):
        create_invoice("test_npub", "test_note")