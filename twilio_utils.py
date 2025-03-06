import os
import logging
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather, Play

# Configure logging
logger = logging.getLogger(__name__)

def get_twilio_client():
    """
    Get a Twilio client using environment variables.
    
    Returns:
        Client: Initialized Twilio client
    """
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    
    if not account_sid or not auth_token:
        logger.warning("Twilio credentials not found in environment variables")
        return None
    
    return Client(account_sid, auth_token)

def generate_twiml_response(response_type):
    """
    Generate TwiML response based on the required response type.
    
    Args:
        response_type (str): Type of response to generate 
                           ('welcome', 'music', 'beep', 'error', 'busy', or 'invalid')
    
    Returns:
        VoiceResponse: TwiML response object
    """
    response = VoiceResponse()
    
    if response_type == "welcome":
        # Welcome message and menu
        response.say("Welcome to the telephony testing service.")
        response.pause(length=1)
        
        gather = Gather(num_digits=1, action="/handle_ivr", method="POST", timeout=10)
        gather.say("Press 1 to listen to music. Press 2 to hear a beep every 3 seconds.")
        response.append(gather)
        
        # If no input, repeat the menu
        response.redirect("/incoming_call")
    
    elif response_type == "music":
        # Play music
        response.say("Playing music now.")
        # Using a URL for music, assuming this is hosted somewhere accessible
        response.play("https://demo.twilio.com/docs/classic.mp3", loop=10)
    
    elif response_type == "beep":
        # Play beep every 3 seconds
        response.say("Playing a beep every 3 seconds.")
        for _ in range(20):  # Loop for about a minute (20 * 3 seconds)
            response.play("https://demo.twilio.com/docs/classic.mp3", loop=1)
            response.pause(length=3)
    
    elif response_type == "error":
        # Error handling
        response.say("We're sorry, but we encountered an error processing your call. Please try again later.")
        response.hangup()
    
    elif response_type == "busy":
        # Busy signal - max calls reached
        response.say("We're sorry, but all lines are currently busy. The maximum number of simultaneous calls has been reached. Please try again later.")
        response.hangup()
    
    elif response_type == "invalid":
        # Invalid selection
        response.say("Sorry, that's not a valid option.")
        
        gather = Gather(num_digits=1, action="/handle_ivr", method="POST", timeout=10)
        gather.say("Press 1 to listen to music. Press 2 to hear a beep every 3 seconds.")
        response.append(gather)
        
        # If no input again, end call
        response.say("No input received. Goodbye.")
        response.hangup()
    
    return response
