# KPLC Notifier 20260624b

An automated Python script to monitor KPLC (Kenya Power) token balances and send SMS alerts via Africa's Talking when units fall below a specific threshold.

## Setup

1. **Clone the repository**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   KPLC_ACCOUNT_NUMBER=12345678901
   KPLC_API_KEY=your_provider_api_key
   AT_USERNAME=sandbox
   AT_API_KEY=your_africas_talking_api_key
   RECIPIENT_PHONE=+254700000000
   LOW_BALANCE_THRESHOLD=15.0
   ```

## Usage

Run the script manually:
```bash
python notifier.py
```

To automate this, set up a cron job (Linux) or Task Scheduler (Windows) to run the script daily or every 6 hours.

## Requirements
- Python 3.8+
- Africa's Talking Account (for SMS alerts)
- Access to a utility provider API for fetching KPLC data (e.g., a payment bridge or utility aggregator).