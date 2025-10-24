"""Transaction processing module for AutoZap.

This module handles payment processing logic, including rate limiting and payment tracking.
"""

import logging
from typing import Optional
from backend.config import config
from backend.db.models import Database
from backend.ln_wallet.wallet import create_invoice, PaymentResult, LNbitsError

logger = logging.getLogger(__name__)

def process_payment(npub: str, note_id: str) -> Optional[PaymentResult]:
    """Process a payment for a repost, including rate limiting checks.
    
    Args:
        npub: The public key of the user to pay
        note_id: The ID of the note being reposted
        
    Returns:
        PaymentResult object if payment was attempted, None if rate limited
    """
    db = Database(config.db_path)
    
    # Check for recent payments to this user for this note
    if db.has_recent_payment(npub, note_id, config.rate_limit_hours):
        logger.info(
            f"Rate limit: User {npub[:8]}... already received payment for "
            f"note {note_id[:8]}... in the last {config.rate_limit_hours} hours"
        )
        return None
    
    try:
        # Generate and process the payment
        result = create_invoice(npub, note_id, config.payment_amount)
        
        if result.success:
            logger.info(
                f"Payment of {config.payment_amount} sat initiated for "
                f"{npub[:8]}... (Note: {note_id[:8]}...)"
            )
        else:
            logger.error(
                f"Payment failed for {npub[:8]}...: {result.error_message}"
            )
            
        return result
        
    except LNbitsError as e:
        logger.error(f"Lightning payment error: {str(e)}")
        return PaymentResult(
            success=False,
            status="failed",
            error_message=str(e)
        )
        
    except Exception as e:
        logger.error(f"Unexpected error processing payment: {str(e)}")
        return PaymentResult(
            success=False,
            status="failed",
            error_message=f"Internal error: {str(e)}"
        )
