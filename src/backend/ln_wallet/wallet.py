"""Lightning Network wallet interface for AutoZap.

This module handles all Lightning Network payment operations through the LNbits API.
"""

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional
import requests
from src.backend.config import config, Config
from src.backend.db.models import Database, Payment

logger = logging.getLogger(__name__)

# Store config instance for testing
_config_instance: Optional[Config] = None

def set_config_for_testing(cfg: Config) -> None:
    """Set configuration for testing purposes.
    
    Args:
        cfg: Configuration instance to use
    """
    global _config_instance
    _config_instance = cfg

@dataclass
class PaymentResult:
    """Container for payment operation results."""
    
    success: bool
    status: str
    bolt11: Optional[str] = None
    payment_hash: Optional[str] = None
    error_message: Optional[str] = None

class LNbitsError(Exception):
    """Base exception for LNbits-related errors."""
    pass

class InvoiceGenerationError(LNbitsError):
    """Raised when invoice generation fails."""
    pass

class PaymentError(LNbitsError):
    """Raised when payment processing fails."""
    pass

def create_invoice(npub: str, note_id: str, amount: Optional[int] = None) -> PaymentResult:
    """Generate a Lightning Network invoice through LNbits.
    
    Args:
        npub: The public key of the user to pay
        note_id: The ID of the note being reposted
        amount: Optional payment amount in satoshis (defaults to config value)
        
    Returns:
        PaymentResult object containing the operation result
        
    Raises:
        InvoiceGenerationError: If invoice generation fails
    """
    cfg = _config_instance or config
    if cfg is None:
        raise InvoiceGenerationError("Configuration not initialized")
        
    if amount is None:
        amount = cfg.payment_amount
            
        headers = {
            "X-Api-Key": cfg.lnbits_api_key,
            "Content-type": "application/json"
        }
        
        invoice_data = {
            "out": False,
            "amount": amount,
            "memo": f"AutoZap payment for repost of {note_id[:8]}... by {npub[:8]}...",
        }

        try:
            response = requests.post(
                f"{cfg.lnbits_url}/api/v1/payments",
                json=invoice_data,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            invoice_result = response.json()
            
            if "payment_request" not in invoice_result:
                raise InvoiceGenerationError("No BOLT11 invoice in response")
                
            bolt11 = invoice_result["payment_request"]
            payment_hash = invoice_result.get("payment_hash")
            
            # Record the payment in the database
            db = Database(cfg.db_path)
            payment = Payment(
                id=None,
                npub=npub,
                amount=amount,
                bolt11=bolt11,
                status="pending",
                created_at=datetime.now(),
                note_id=note_id
            )
            db.add_payment(payment)
            
            logger.info(
                f"Invoice generated for {amount} sat to {npub[:8]}... "
                f"for note {note_id[:8]}..."
            )
            
            return PaymentResult(
                success=True,
                status="invoice_generated",
                bolt11=bolt11,
                payment_hash=payment_hash
            )

        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to connect to LNbits: {str(e)}"
            logger.error(error_msg)
            raise InvoiceGenerationError(error_msg) from e
            
        except Exception as e:
            error_msg = f"Unexpected error generating invoice: {str(e)}"
            logger.error(error_msg)
            raise InvoiceGenerationError(error_msg) from e
