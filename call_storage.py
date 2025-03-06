"""
In-memory storage for active calls.
This module replaces the database-based call storage with a simpler in-memory solution.
"""

from datetime import datetime
import threading

# Thread-safe dictionary to store active calls
# Key: call_sid, Value: call data dictionary
_active_calls = {}
_lock = threading.RLock()  # Reentrant lock for thread safety

def add_call(call_sid, from_number, to_number):
    """
    Add a new call to the active calls storage.
    
    Args:
        call_sid (str): The Twilio call SID
        from_number (str): The caller's phone number
        to_number (str): The called phone number
    
    Returns:
        dict: The created call record
    """
    with _lock:
        call_data = {
            'call_sid': call_sid,
            'from_number': from_number,
            'to_number': to_number,
            'start_time': datetime.utcnow().isoformat(),
            'ivr_selection': None
        }
        _active_calls[call_sid] = call_data
        return call_data.copy()

def update_ivr_selection(call_sid, selection):
    """
    Update the IVR selection for a call.
    
    Args:
        call_sid (str): The Twilio call SID
        selection (str): The IVR selection ('music' or 'beep')
    
    Returns:
        dict: The updated call record or None if not found
    """
    with _lock:
        if call_sid in _active_calls:
            _active_calls[call_sid]['ivr_selection'] = selection
            return _active_calls[call_sid].copy()
        return None

def end_call(call_sid):
    """
    Remove a call from active calls when it ends.
    
    Args:
        call_sid (str): The Twilio call SID
    
    Returns:
        dict: The call data that was removed, or None if not found
    """
    with _lock:
        if call_sid in _active_calls:
            call_data = _active_calls.pop(call_sid)
            return call_data
        return None

def get_active_calls():
    """
    Get all active calls.
    
    Returns:
        list: List of active calls as dictionaries
    """
    with _lock:
        return list(_active_calls.values())

def get_call_count():
    """
    Get count of active calls.
    
    Returns:
        int: Number of active calls
    """
    with _lock:
        return len(_active_calls)

def get_call(call_sid):
    """
    Get a specific call by SID.
    
    Args:
        call_sid (str): The Twilio call SID
    
    Returns:
        dict: Call data or None if not found
    """
    with _lock:
        return _active_calls.get(call_sid, {}).copy()