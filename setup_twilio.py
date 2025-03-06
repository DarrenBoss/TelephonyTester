"""
Setup script to help add Twilio credentials to Replit Secrets.
"""
import os
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_twilio():
    """
    Interactive script to configure Twilio credentials in environment.
    This script will guide the user through setting up their Twilio credentials.
    """
    print("\n=== Twilio Configuration Utility ===\n")
    print("This script will help you set up your Twilio credentials.")
    print("Note: Your credentials will be displayed in the terminal as you type them.")
    print("These credentials will be saved to your Replit Secrets.\n")
    
    # Check existing configuration
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID', '')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN', '')
    phone_number = os.environ.get('TWILIO_PHONE_NUMBER', '')
    base_url = os.environ.get('BASE_URL', '')
    
    if account_sid:
        print(f"Found existing Twilio Account SID: {account_sid[:5]}...{account_sid[-5:]}")
    else:
        print("No Twilio Account SID configured.")
    
    if auth_token:
        print(f"Found existing Twilio Auth Token: {auth_token[:3]}...{auth_token[-3:]}")
    else:
        print("No Twilio Auth Token configured.")
    
    if phone_number:
        print(f"Found existing Twilio Phone Number: {phone_number}")
    else:
        print("No Twilio Phone Number configured.")
    
    if base_url:
        print(f"Found existing Base URL: {base_url}")
    else:
        print("No Base URL configured.")
    
    print("\nWould you like to update these settings? (yes/no)")
    answer = input().strip().lower()
    
    if answer != "yes" and answer != "y":
        print("Setup canceled.")
        return
    
    print("\n=== Enter your Twilio credentials ===")
    print("You can find these in your Twilio Console: https://www.twilio.com/console")
    
    # Get Account SID
    print("\nEnter your Twilio Account SID:")
    account_sid = input().strip()
    
    # Get Auth Token
    print("\nEnter your Twilio Auth Token:")
    auth_token = input().strip()
    
    # Get Phone Number (optional)
    print("\nEnter your Twilio Phone Number (optional):")
    print("Format: +15551234567")
    phone_number = input().strip()
    
    # Get Base URL (optional)
    print("\nEnter the Base URL for your Replit app (optional):")
    print("Example: https://your-app-name.replit.app")
    base_url = input().strip()
    
    print("\nPlease verify your information:")
    print(f"Twilio Account SID: {account_sid[:5]}...{account_sid[-5:]}")
    print(f"Twilio Auth Token: {auth_token[:3]}...{auth_token[-3:]}")
    if phone_number:
        print(f"Twilio Phone Number: {phone_number}")
    if base_url:
        print(f"Base URL: {base_url}")
    
    print("\nSave these settings to Replit Secrets? (yes/no)")
    confirm = input().strip().lower()
    
    if confirm != "yes" and confirm != "y":
        print("Setup canceled.")
        return
    
    # Output instructions for setting Replit Secrets
    print("\n=== Instructions to save your credentials ===")
    print("Since this script cannot directly update your Replit Secrets, please follow these steps:")
    
    print("\n1. Click on the Tools icon in the Replit sidebar (looks like a wrench)")
    print("2. Click on 'Secrets'")
    print("3. Add the following key-value pairs:")
    
    print(f"\n   Key: TWILIO_ACCOUNT_SID")
    print(f"   Value: {account_sid}")
    
    print(f"\n   Key: TWILIO_AUTH_TOKEN")
    print(f"   Value: {auth_token}")
    
    if phone_number:
        print(f"\n   Key: TWILIO_PHONE_NUMBER")
        print(f"   Value: {phone_number}")
    
    if base_url:
        print(f"\n   Key: BASE_URL")
        print(f"   Value: {base_url}")
    
    print("\nAfter adding these secrets, restart your application for the changes to take effect.")
    print("You can restart by either:")
    print("1. Clicking the 'Stop' and then 'Run' button at the top of the Replit interface, or")
    print("2. Entering 'Run' in the command palette (Ctrl+Shift+P or Cmd+Shift+P on macOS)") 
    
    print("\nSetup complete! Follow the instructions above to save your credentials.")

if __name__ == "__main__":
    setup_twilio()