# AutoZap

AutoZap is a sophisticated bot for the Nostr network that monitors reposts of specific notes and automatically rewards users with Lightning Network payments (zaps). Built with Python and powered by LNbits, it enables automated engagement rewards in the Nostr ecosystem.

## 🌟 Features

- **Automated Repost Monitoring**: Track specific notes across multiple Nostr relays
- **Lightning Rewards**: Instant payments to users who engage with content
- **Rate Limiting**: Prevent abuse with configurable payment timeouts
- **Payment Tracking**: SQLite database for tracking all transactions
- **Robust Error Handling**: Comprehensive error recovery and logging
- **Type Safety**: Full Python type hints for code reliability

## 🔧 Technical Stack

- **Python** 3.10+
- **Nostr**: For decentralized social networking
- **LNbits**: Lightning Network payment processing
- **SQLite**: Local payment tracking database
- **Type Hints**: Python typing for code safety

## 📋 Prerequisites

1. **Python Environment**: Python 3.10 or higher
2. **LNbits Account**: Access to a LNbits instance for payment processing
3. **Nostr Account**: Access to Nostr relays
4. **System Requirements**: 
   - Linux/macOS/Windows
   - 512MB RAM minimum
   - 1GB disk space

## 🚀 Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/NOSTR-HUB/AutoZap.git
   cd AutoZap
   ```

2. **Create Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   .\\venv\\Scripts\\activate  # Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**:
   ```bash
   cp config/.env.example .env
   ```
   
   Edit `.env` with your settings:
   ```env
   # LNbits Configuration
   LNBITS_API_KEY=your_api_key
   LNBITS_URL=https://your.lnbits.instance
   
   # Nostr Configuration
   NOSTR_RELAY_URLS=wss://relay1.com,wss://relay2.com
   
   # Payment Settings
   PAYMENT_AMOUNT=1000  # Amount in satoshis
   RATE_LIMIT_HOURS=24  # Hours between payments to same user
   DB_PATH=payments.db  # SQLite database path
   ```

## 🎮 Usage

1. **Start the Bot**:
   ```bash
   # Ensure virtual environment is active
   source venv/bin/activate
   
   # Run the bot
   PYTHONPATH=$(pwd)/src python3 -m backend.nostr_bot.bot
   ```

2. **Monitor Operation**:
   - Check logs for operation status
   - View payment history in SQLite database
   - Monitor LNbits wallet balance

3. **Configuration Options**:
   | Setting | Description | Default |
   |---------|-------------|---------|
   | `PAYMENT_AMOUNT` | Satoshis per payment | 1000 |
   | `RATE_LIMIT_HOURS` | Hours between payments | 24 |
   | `DB_PATH` | Database location | payments.db |

## 📊 Database Schema

The SQLite database (`payments.db`) tracks all payments:

```sql
CREATE TABLE payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    npub TEXT NOT NULL,
    amount INTEGER NOT NULL,
    bolt11 TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    note_id TEXT NOT NULL
);
```

## 🛠 Development

1. **Type Checking**:
   ```bash
   mypy src/
   ```

2. **Run Tests**:
   ```bash
   pytest tests/
   ```

3. **Code Style**:
   ```bash
   black src/
   flake8 src/
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

Please ensure your PR:
- Includes type hints
- Adds tests for new features
- Updates documentation
- Follows code style guidelines

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 🔍 Troubleshooting

### Common Issues

1. **Connection Errors**:
   - Check relay URLs are valid and accessible
   - Verify internet connection
   - Ensure websocket support

2. **Payment Failures**:
   - Verify LNbits API key and URL
   - Check wallet balance
   - Confirm rate limits

3. **Database Issues**:
   - Check write permissions
   - Verify SQLite installation
   - Check disk space

### Debug Mode

Enable debug logging:
```bash
export LOG_LEVEL=DEBUG
```

## 📚 API Documentation

See [API.md](docs/API.md) for detailed API documentation.

## 🔐 Security

- All payments are rate-limited by user and note
- API keys are loaded from environment only
- SQLite database prevents SQL injection
- Input validation on all external data

## 📦 Project Structure

```
AutoZap/
├── src/
│   └── backend/
│       ├── config.py      # Configuration management
│       ├── db/
│       │   └── models.py  # Database models
│       ├── ln_wallet/
│       │   └── wallet.py  # Lightning payment handling
│       └── nostr_bot/
│           ├── bot.py     # Main bot logic
│           ├── events.py  # Event processing
│           └── transactions.py  # Payment processing
├── tests/                 # Test suite
├── docs/                  # Documentation
└── config/
    └── settings.py        # Default settings
```
