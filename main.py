import logging
import os
from load_env import load_env_variables
from app import app

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Load environment variables from Replit Secrets
load_env_variables()

# Log current Twilio configuration status (without exposing sensitive data)
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
if account_sid:
    # Safely mask the SID to avoid exposing the full value in logs
    if len(account_sid) > 10:
        masked_sid = f"{account_sid[:5]}...{account_sid[-5:]}"
    else:
        masked_sid = "***" 
    logging.info(f"Twilio Account SID configured: {masked_sid}")
else:
    logging.warning("Twilio Account SID not found in environment")

if os.environ.get('TWILIO_AUTH_TOKEN'):
    logging.info("Twilio Auth Token configured")
else:
    logging.warning("Twilio Auth Token not found in environment")

if os.environ.get('BASE_URL'):
    logging.info(f"Base URL configured: {os.environ.get('BASE_URL')}")
else:
    logging.warning("Base URL not configured")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
