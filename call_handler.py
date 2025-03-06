import logging
from datetime import datetime
import json
from call_storage import (
    add_call,
    end_call,
    update_ivr_selection,
    get_active_calls as get_calls,
    get_call_count as get_count,
    get_call
)

# Configure logging
logger = logging.getLogger(__name__)

def handle_call_start(call_sid, from_number, to_number):
    """
    Handle a new incoming call.
    
    Args:
        call_sid (str): The Twilio call SID
        from_number (str): The caller's phone number
        to_number (str): The called phone number
    
    Returns:
        dict: The created call record
    """
    try:
        # Check if call already exists
        existing_call = get_call(call_sid)
        if existing_call and existing_call.get('call_sid'):
            logger.warning(f"Call with SID {call_sid} already exists")
            return existing_call
        
        # Create new call record
        new_call = add_call(call_sid, from_number, to_number)
        logger.info(f"New call created: {call_sid} from {from_number}")
        
        return new_call
    
    except Exception as e:
        logger.error(f"Error handling call start: {str(e)}")
        raise

def handle_call_end(call_sid):
    """
    Handle call completion.
    
    Args:
        call_sid (str): The Twilio call SID
    
    Returns:
        dict: The removed call record
    """
    try:
        # Remove call from active calls
        call = end_call(call_sid)
        
        if not call:
            logger.warning(f"Call with SID {call_sid} not found for call end")
            return None
        
        logger.info(f"Call ended: {call_sid}")
        return call
    
    except Exception as e:
        logger.error(f"Error handling call end: {str(e)}")
        raise

def update_call_ivr(call_sid, selection):
    """
    Update the IVR selection for a call.
    
    Args:
        call_sid (str): The Twilio call SID
        selection (str): The IVR selection ('music' or 'beep')
    
    Returns:
        dict: The updated call record
    """
    try:
        call = update_ivr_selection(call_sid, selection)
        if not call:
            logger.warning(f"Call with SID {call_sid} not found for IVR update")
            return None
        
        logger.info(f"Call {call_sid} updated with IVR selection: {selection}")
        return call
    
    except Exception as e:
        logger.error(f"Error updating call IVR: {str(e)}")
        raise

def get_active_calls():
    """
    Get all active calls.
    
    Returns:
        list: List of active calls as dictionaries
    """
    try:
        return get_calls()
    
    except Exception as e:
        logger.error(f"Error getting active calls: {str(e)}")
        return []

def get_call_count():
    """
    Get count of active calls.
    
    Returns:
        int: Number of active calls
    """
    try:
        return get_count()
    
    except Exception as e:
        logger.error(f"Error getting call count: {str(e)}")
        return 0
