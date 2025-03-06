import os
import logging

logger = logging.getLogger(__name__)

def load_env_variables():
    """
    Loads environment variables from Replit Secrets.
    This function doesn't need to do anything special since Replit 
    automatically loads secrets into the environment.
    """
    # Check if important variables are available
    required_vars = ['TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        logger.warning(f"Missing environment variables: {', '.join(missing_vars)}")
        logger.warning("Make sure to set these in Replit Secrets for the application to work properly.")
    else:
        logger.info("All required environment variables found.")
    
    # Set default BASE_URL if not provided
    if not os.environ.get('BASE_URL'):
        # Get the REPLIT_SLUG and REPL_OWNER from the environment
        replit_slug = os.environ.get('REPLIT_SLUG', '')
        repl_owner = os.environ.get('REPL_OWNER', '')
        
        if replit_slug and repl_owner:
            default_url = f"https://{replit_slug}.{repl_owner}.repl.co"
            os.environ['BASE_URL'] = default_url
            logger.info(f"BASE_URL not provided, using default: {default_url}")
        else:
            # Fallback to a generic default
            default_url = "https://telephony-test-platform.replit.app"
            os.environ['BASE_URL'] = default_url
            logger.info(f"BASE_URL not provided, using fallback: {default_url}")