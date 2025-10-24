"""Test payment database operations."""

import pytest
import sqlite3
from datetime import datetime, timedelta
from src.backend.db.models import Database, Payment

@pytest.fixture
def test_db():
    """Create a test database instance."""
    conn = sqlite3.connect(":memory:")
    db = Database(":memory:")
    db.connection = conn  # Keep the connection persistent for in-memory database
    db._create_tables(conn)
    return db

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
    from datetime import datetime
    
    # Add a test payment
    payment = Payment(
        id=None,
        npub="test_npub",
        amount=1000,
        bolt11="test_bolt11",
        status="paid",
        created_at=datetime.now(),
        note_id="test_note"
    )
    test_db.add_payment(payment)
    
    # Check for recent payment
    assert test_db.has_recent_payment("test_npub", "test_note", 24)
    assert not test_db.has_recent_payment("other_npub", "test_note", 24)

def test_get_payment_history(test_db):
    """Test retrieving payment history."""
    from datetime import datetime
    
    now = datetime.now()
    # Add multiple test payments
    payments = [
        Payment(None, "npub1", 1000, "bolt11_1", "paid", now, "note1"),
        Payment(None, "npub1", 2000, "bolt11_2", "paid", now, "note2"),
        Payment(None, "npub2", 1500, "bolt11_3", "paid", now, "note1")
    ]
    
    for payment in payments:
        test_db.add_payment(payment)
    
    # Test getting all payments
    all_history = test_db.get_payment_history()
    assert len(all_history) == 3
    
    # Test getting payments for specific user
    user_history = test_db.get_payment_history("npub1")
    assert len(user_history) == 2