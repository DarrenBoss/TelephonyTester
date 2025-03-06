import logging
from datetime import datetime
from app import db, app
from models import Call
import json

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
        Call: The created Call record
    """
    try:
        with app.app_context():
            # Check if call already exists
            existing_call = Call.query.filter_by(call_sid=call_sid).first()
            
            if existing_call:
                logger.warning(f"Call with SID {call_sid} already exists")
                return existing_call
            
            # Create new call record
            new_call = Call(
                call_sid=call_sid,
                from_number=from_number,
                to_number=to_number,
                start_time=datetime.utcnow(),
                is_active=True
            )
            
            db.session.add(new_call)
            db.session.commit()
            logger.info(f"New call created: {call_sid} from {from_number}")
            
            # Since we're using direct SSE without Redis, no need to publish updates here
            # The client will poll the SSE endpoint for updates
            
            return new_call
    
    except Exception as e:
        logger.error(f"Error handling call start: {str(e)}")
        db.session.rollback()
        raise

def handle_call_end(call_sid):
    """
    Handle call completion.
    
    Args:
        call_sid (str): The Twilio call SID
    
    Returns:
        Call: The updated Call record
    """
    try:
        with app.app_context():
            call = Call.query.filter_by(call_sid=call_sid).first()
            
            if not call:
                logger.warning(f"Call with SID {call_sid} not found for call end")
                return None
            
            call.is_active = False
            call.end_time = datetime.utcnow()
            db.session.commit()
            logger.info(f"Call ended: {call_sid}")
            
            # Since we're using direct SSE without Redis, no need to publish updates here
            # The client will poll the SSE endpoint for updates
            
            return call
    
    except Exception as e:
        logger.error(f"Error handling call end: {str(e)}")
        db.session.rollback()
        raise

def get_active_calls():
    """
    Get all active calls.
    
    Returns:
        list: List of active calls as dictionaries
    """
    try:
        with app.app_context():
            calls = Call.query.filter_by(is_active=True).all()
            return [call.to_dict() for call in calls]
    
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
        with app.app_context():
            return Call.query.filter_by(is_active=True).count()
    
    except Exception as e:
        logger.error(f"Error getting call count: {str(e)}")
        return 0
