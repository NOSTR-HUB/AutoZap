# Use a slim Python base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create volume for persistent data
VOLUME ["/app/data"]

# Set environment variables with defaults
ENV LNBITS_API_KEY=""
ENV LNBITS_URL=""
ENV NOSTR_RELAY_URLS=""
ENV PAYMENT_AMOUNT="1000"
ENV RATE_LIMIT_HOURS="24"
ENV DB_PATH="/app/data/payments.db"
ENV LOG_LEVEL="INFO"

# Run the bot
CMD ["python", "-m", "src.backend.nostr_bot.bot"]