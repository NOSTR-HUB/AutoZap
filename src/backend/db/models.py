"""Database models for AutoZap payment tracking."""

from datetime import datetime
import sqlite3
from typing import Optional
from dataclasses import dataclass

@dataclass
class Payment:
    """Represents a Lightning Network payment made by the bot."""
    id: Optional[int]
    npub: str
    amount: int
    bolt11: str
    status: str
    created_at: datetime
    note_id: str

class Database:
    """Handles database operations for payment tracking."""
    
    def __init__(self, db_path: str = "payments.db"):
        """Initialize database connection and create tables if they don't exist.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.connection = None  # For persistent connections in tests
        conn = sqlite3.connect(self.db_path)
        self._create_tables(conn)
        conn.close()
    
    def _create_tables(self, conn: sqlite3.Connection):
        """Create necessary database tables if they don't exist.
        
        Args:
            conn: SQLite database connection
        """
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            npub TEXT NOT NULL,
            amount INTEGER NOT NULL,
            bolt11 TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            note_id TEXT NOT NULL
        )
        """)
        
        conn.commit()
    
    def add_payment(self, payment: Payment) -> int:
        """Add a new payment record to the database.
        
        Args:
            payment: Payment object containing payment details
            
        Returns:
            The ID of the inserted payment record
        """
        conn = self.connection or sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            if not self.connection:
                self._create_tables(conn)  # Ensure tables exist
            
            created_at = payment.created_at or datetime.now()
            cursor.execute("""
            INSERT INTO payments (npub, amount, bolt11, status, note_id, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (payment.npub, payment.amount, payment.bolt11, payment.status, payment.note_id, created_at))
            
            payment_id = cursor.lastrowid
            conn.commit()
            return payment_id
        finally:
            if not self.connection:
                conn.close()
    
    def has_recent_payment(self, npub: str, note_id: str, hours: int = 24) -> bool:
        """Check if a user has received a payment for a specific note in the recent past.
        
        Args:
            npub: The user's public key
            note_id: The ID of the note being reposted
            hours: Number of hours to look back (default: 24)
            
        Returns:
            True if a recent payment exists, False otherwise
        """
        conn = self.connection or sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            if not self.connection:
                self._create_tables(conn)  # Ensure tables exist
            
            cursor.execute("""
            SELECT COUNT(*) FROM payments 
            WHERE npub = ? AND note_id = ? 
            AND created_at >= datetime('now', '-' || ? || ' hours')
            AND status = 'paid'
            """, (npub, note_id, hours))
            
            count = cursor.fetchone()[0]
            return count > 0
        finally:
            if not self.connection:
                conn.close()
    
    def get_payment_history(self, npub: Optional[str] = None) -> list[Payment]:
        """Get payment history, optionally filtered by user.
        
        Args:
            npub: Optional public key to filter payments by user
            
        Returns:
            List of Payment objects representing the payment history
        """
        conn = self.connection or sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            if not self.connection:
                self._create_tables(conn)  # Ensure tables exist
            
            if npub:
                cursor.execute("""
                SELECT id, npub, amount, bolt11, status, created_at, note_id 
                FROM payments WHERE npub = ? ORDER BY created_at DESC
                """, (npub,))
            else:
                cursor.execute("""
                SELECT id, npub, amount, bolt11, status, created_at, note_id 
                FROM payments ORDER BY created_at DESC
                """)
                
            rows = cursor.fetchall()
            
            return [
                Payment(
                    id=row[0],
                    npub=row[1],
                    amount=row[2],
                    bolt11=row[3],
                    status=row[4],
                    created_at=datetime.fromisoformat(row[5]),
                    note_id=row[6]
                )
                for row in rows
            ]
        finally:
            if not self.connection:
                conn.close()