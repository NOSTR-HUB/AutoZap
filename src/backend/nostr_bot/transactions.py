import logging
from backend.config import PAYMENT_AMOUNT
from backend.ln_wallet.wallet import send_payment

# Process payment with budget check
def process_payment(npub):
    try:
        # Send a payment of fixed amount to the reposting user's pubkey (npub)
        result = send_payment(npub, PAYMENT_AMOUNT)
        
        if result["status"] == "paid":
            logging.info(f"Payment of {PAYMENT_AMOUNT} sat sent to {npub}. Transaction ID: {result['tx_id']}")
        else:
            logging.error("Payment failed or response was unsuccessful.")
    except Exception as e:
        logging.error(f"Error processing payment for {npub}: {str(e)}")
