import os
import logging
import requests
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class KPLCNotifier:
    def __init__(self):
        load_dotenv()
        self.account_number = os.getenv('KPLC_ACCOUNT_NUMBER')
        self.api_key = os.getenv('KPLC_API_KEY')
        self.at_username = os.getenv('AT_USERNAME')
        self.at_api_key = os.getenv('AT_API_KEY')
        self.phone_number = os.getenv('RECIPIENT_PHONE')
        self.threshold = float(os.getenv('LOW_BALANCE_THRESHOLD', '10.0'))
        
        # API Endpoints (Placeholders for actual KPLC integration providers)
        self.kplc_api_url = "https://api.utility-checker.co.ke/v1/kplc/balance"
        self.sms_url = "https://api.africastalking.com/version1/messaging"

    def get_token_balance(self):
        """
        Fetches the current token balance from the provider.
        Note: Actual KPLC integration usually requires a 3rd party bridge API.
        """
        logger.info(f"Checking balance for account: {self.account_number}")
        try:
            # This simulates a request to a utility provider API
            params = {"account": self.account_number, "apikey": self.api_key}
            response = requests.get(self.kplc_api_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return float(data.get("balance", 0))
            else:
                logger.error(f"Failed to fetch balance: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error connecting to KPLC provider: {e}")
            return None

    def send_sms_alert(self, balance):
        """
        Sends an SMS alert via Africa's Talking API.
        """
        logger.info(f"Sending low balance alert: {balance} units remaining.")
        headers = {
            "ApiKey": self.at_api_key,
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        }
        
        message = f"KPLC ALERT: Your token balance for account {self.account_number} is low: {balance} units left."
        data = {
            "username": self.at_username,
            "to": self.phone_number,
            "message": message
        }

        try:
            response = requests.post(self.sms_url, headers=headers, data=data, timeout=10)
            if response.status_code == 201:
                logger.info("SMS alert sent successfully.")
            else:
                logger.error(f"Failed to send SMS: {response.text}")
        except Exception as e:
            logger.error(f"Error sending SMS: {e}")

    def check_and_notify(self):
        """
        Main execution logic.
        """
        if not all([self.account_number, self.at_api_key, self.phone_number]):
            logger.error("Missing environment variables. Please check your .env file.")
            return

        balance = self.get_token_balance()
        
        if balance is not None:
            logger.info(f"Current Balance: {balance} Units")
            if balance <= self.threshold:
                self.send_sms_alert(balance)
            else:
                logger.info("Balance is sufficient. No alert sent.")
        else:
            logger.warning("Could not retrieve balance. Skipping notification.")

if __name__ == "__main__":
    notifier = KPLCNotifier()
    notifier.check_and_notify()