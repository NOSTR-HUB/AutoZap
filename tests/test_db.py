"""Test payment database operations."""

import pytest
from datetime import datetime, timedelta
from backend.db.models import Database, Payment

@pytest.fixture
def test_db():
    """Create a test database instance."""
    return Database(":memory:")  # Use in-memory SQLite for testing

def test_add_payment(test_db):
    """Test adding a payment record."""
    payment = Payment(
        id=None,
        npub="test_npub",
        amount=1000,
        bolt11="test_bolt11",
        status="pending",
        created_at=None,
        note_id="test_note"
    )
    
    payment_id = test_db.add_payment(payment)
    assert payment_id > 0

def test_has_recent_payment(test_db):
    """Test checking for recent payments."""
    # Add a test payment
    payment = Payment(
        id=None,
        npub="test_npub",
        amount=1000,
        bolt11="test_bolt11",
        status="paid",
        created_at=None,
        note_id="test_note"
    )
    test_db.add_payment(payment)
    
    # Check for recent payment
    assert test_db.has_recent_payment("test_npub", "test_note", 24)
    assert not test_db.has_recent_payment("other_npub", "test_note", 24)

def test_get_payment_history(test_db):
    """Test retrieving payment history."""
    # Add multiple test payments
    payments = [
        Payment(None, "npub1", 1000, "bolt11_1", "paid", None, "note1"),
        Payment(None, "npub1", 2000, "bolt11_2", "paid", None, "note2"),
        Payment(None, "npub2", 1500, "bolt11_3", "paid", None, "note1")
    ]
    
    for payment in payments:
        test_db.add_payment(payment)
    
    # Test getting all payments
    all_history = test_db.get_payment_history()
    assert len(all_history) == 3
    
    # Test getting payments for specific user
    user_history = test_db.get_payment_history("npub1")
    assert len(user_history) == 2