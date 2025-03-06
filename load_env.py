import os
import logging
import subprocess

logger = logging.getLogger(__name__)

def load_env_variables():
    """
    Loads environment variables from Replit Secrets.
    Checks for variables with alternative names and standardizes them.
    """
    # Define all possible variable names for Twilio credentials
    twilio_sid_vars = ['TWILIO_ACCOUNT_SID', 'TWILIO_SID', 'TWILIO_ACCT_SID']
    twilio_token_vars = ['TWILIO_AUTH_TOKEN', 'TWILIO_TOKEN', 'TWILIO_AUTH']
    twilio_phone_vars = ['TWILIO_PHONE_NUMBER', 'TWILIO_PHONE', 'TWILIO_NUMBER']
    
    # Check for SID with alternative names
    twilio_sid = None
    for var in twilio_sid_vars:
        if os.environ.get(var):
            twilio_sid = os.environ.get(var)
            if var != 'TWILIO_ACCOUNT_SID':
                logger.info(f"Found Twilio SID in {var}, standardizing to TWILIO_ACCOUNT_SID")
                os.environ['TWILIO_ACCOUNT_SID'] = twilio_sid
            break
    
    # Check for token with alternative names
    twilio_token = None
    for var in twilio_token_vars:
        if os.environ.get(var):
            twilio_token = os.environ.get(var)
            if var != 'TWILIO_AUTH_TOKEN':
                logger.info(f"Found Twilio Auth Token in {var}, standardizing to TWILIO_AUTH_TOKEN")
                os.environ['TWILIO_AUTH_TOKEN'] = twilio_token
            break
    
    # Check for phone number with alternative names
    twilio_phone = None
    for var in twilio_phone_vars:
        if os.environ.get(var):
            twilio_phone = os.environ.get(var)
            if var != 'TWILIO_PHONE_NUMBER':
                logger.info(f"Found Twilio Phone Number in {var}, standardizing to TWILIO_PHONE_NUMBER")
                os.environ['TWILIO_PHONE_NUMBER'] = twilio_phone
            break
    
    # Report missing required variables
    missing_vars = []
    if not twilio_sid:
        missing_vars.append('TWILIO_ACCOUNT_SID')
    if not twilio_token:
        missing_vars.append('TWILIO_AUTH_TOKEN')
    
    if missing_vars:
        logger.warning(f"Missing environment variables: {', '.join(missing_vars)}")
        logger.warning("Make sure to set these in Replit Secrets for the application to work properly.")
    else:
        logger.info("All required environment variables found.")
    
    # Set default BASE_URL if not provided
    if not os.environ.get('BASE_URL'):
        # Try to determine the Replit URL
        try:
            # First check if REPL_SLUG and REPL_OWNER are available (newer Replit environments)
            replit_slug = os.environ.get('REPLIT_SLUG', '')
            repl_owner = os.environ.get('REPL_OWNER', '')
            
            if replit_slug and repl_owner:
                default_url = f"https://{replit_slug}.{repl_owner}.repl.co"
                os.environ['BASE_URL'] = default_url
                logger.info(f"BASE_URL not provided, using default: {default_url}")
            else:
                # Try to get the domain from Replit environment (newer approach)
                replit_domain = os.environ.get('REPLIT_DEPLOYMENT_DOMAIN', '')
                if replit_domain:
                    default_url = f"https://{replit_domain}"
                    os.environ['BASE_URL'] = default_url
                    logger.info(f"BASE_URL not provided, using domain: {default_url}")
                else:
                    # Fallback to a generic default
                    default_url = "https://telephony-test-platform.replit.app"
                    os.environ['BASE_URL'] = default_url
                    logger.info(f"BASE_URL not provided, using fallback: {default_url}")
        except Exception as e:
            logger.error(f"Error determining BASE_URL: {str(e)}")
            # Fallback to a generic default
            default_url = "https://telephony-test-platform.replit.app"
            os.environ['BASE_URL'] = default_url
            logger.info(f"BASE_URL not provided, using fallback: {default_url}")