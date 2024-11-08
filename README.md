# AutoZap

AutoZap is a bot for the Nostr network designed to monitor reposts of specific notes and automatically send small Lightning Network payments (zaps) to users who engage with these notes. It's powered by Python, Nostr libraries, and LNbits for Lightning transactions.

## Features

- Monitors Nostr relays for reposts of specific notes.
- Automatically sends payments (zaps) to users when they engage.
- Uses LNbits API for handling Lightning payments.

## Prerequisites

- **Python** 3.10 or higher
- **Virtual Environment** (optional but recommended)
- **Nostr Account** with relays
- **LNbits Account** for handling Lightning payments

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/NOSTR-HUB/AutoZap.git
   cd AutoZap
   ```

2. **Set up the virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration:**

   Create a `.env` file in the root directory to configure environment variables:

   ```bash
   cp config/.env.example .env
   ```

   Edit `.env` with your preferred editor to include the following values:

   - `LNBITS_API_KEY`: Your LNbits API key.
   - `LNBITS_URL`: Your LNbits instance URL for creating invoices.
   - `NOSTR_RELAY_URLS`: Comma-separated list of Nostr relay URLs.
   - `PAYMENT_AMOUNT`: The amount in satoshis to send for each qualifying repost.

## Usage

1. **Activate the virtual environment (if not already active):**

   ```bash
   source venv/bin/activate
   ```

2. **Run the bot:**

   ```bash
   PYTHONPATH=$(pwd)/src python3 -m backend.nostr_bot.bot
   ```

   The bot will connect to configured Nostr relays, listen for reposts of the specified note, and trigger payments.

## Contributing

If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are welcome.

## License

This project is licensed under the MIT License.

## Troubleshooting

- **LNbits Payment Error**: Ensure that the `LNBITS_API_KEY` and `LNBITS_URL` are correctly set in your `.env` file.
- **Nostr Relay Connection Issues**: Verify that the relays listed in `NOSTR_RELAY_URLS` are reachable.
