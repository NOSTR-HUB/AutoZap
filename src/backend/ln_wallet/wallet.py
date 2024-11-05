import requests
import logging
from config import LNBITS_API_KEY, LNBITS_URL

# Send payment through LNBits
def send_payment(npub, amount):
    headers = {"X-Api-Key": LNBITS_API_KEY, "Content-type": "application/json"}
    data = {
        "out": False,        # Set to False for creating invoices (paying out)
        "amount": amount,    # Amount in sats to send
        "memo": f"Payment for repost from {npub}",
    }

    response = requests.post(LNBITS_URL, json=data, headers=headers)
    
    if response.status_code == 200:
        payment_result = response.json()
        return {
            "status": "paid" if payment_result.get("paid") else "failed",
            "tx_id": payment_result.get("payment_hash", None)
        }
    else:
        logging.error(f"LNBits payment failed with status {response.status_code}: {response.text}")
        return {"status": "failed"}
