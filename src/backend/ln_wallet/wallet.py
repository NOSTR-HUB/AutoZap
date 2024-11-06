import requests
import logging
from backend.config import LNBITS_API_KEY, LNBITS_URL, PAYMENT_AMOUNT

# Generate an invoice in LNbits
def send_payment(npub, amount=PAYMENT_AMOUNT):
    headers = {
        "X-Api-Key": LNBITS_API_KEY,
        "Content-type": "application/json"
    }

    # Step 1: Generate an invoice (payable to LNbits wallet)
    invoice_data = {
        "out": False,                  # Set to False to create a receivable invoice
        "amount": amount,              # Sats to be received
        "memo": f"Payment for repost by {npub}",  # Memo for the transaction
    }

    try:
        # Request an invoice from LNbits
        response = requests.post(f"{LNBITS_URL}/api/v1/payments", json=invoice_data, headers=headers)

        if response.status_code in (200, 201):  # Accept both 200 and 201 as successful responses
            invoice_result = response.json()
            bolt11 = invoice_result.get("payment_request")

            if bolt11:
                logging.info(f"Invoice generated for {amount} sat to {npub}. BOLT11: {bolt11}")
                return {"status": "invoice_generated", "bolt11": bolt11}
            else:
                logging.error("Invoice generation failed: No BOLT11 string received.")
                return {"status": "failed"}
        else:
            logging.error(f"LNbits invoice request failed with status {response.status_code}: {response.text}")
            return {"status": "failed"}

    except requests.exceptions.RequestException as e:
        logging.error(f"Error connecting to LNbits for invoice generation: {e}")
        return {"status": "failed"}
