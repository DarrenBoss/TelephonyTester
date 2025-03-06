import os
import logging
from flask import Flask, render_template, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import json
import time
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)

# Setup database
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "telephony-test-app-secret")

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///telephony.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the app with the extension
db.init_app(app)

# Import routes after app initialization to avoid circular imports
from models import Call
from twilio_utils import generate_twiml_response, get_twilio_client
from call_handler import handle_call_start, handle_call_end, get_active_calls, get_call_count

with app.app_context():
    # Create database tables
    db.create_all()

@app.route('/')
def dashboard():
    """Render the dashboard page."""
    return render_template('dashboard.html')

@app.route('/incoming_call', methods=['POST'])
def incoming_call():
    """Handle incoming calls from Twilio."""
    try:
        # Extract call data
        call_sid = request.values.get('CallSid', 'unknown')
        from_number = request.values.get('From', 'unknown')
        to_number = request.values.get('To', 'unknown')
        
        logger.debug(f"Incoming call from {from_number} to {to_number} with SID {call_sid}")
        
        # Check if we can accept more calls
        active_calls = get_call_count()
        if active_calls >= 20:
            logger.warning(f"Max calls reached ({active_calls}/20). Rejecting call from {from_number}")
            response = generate_twiml_response("busy")
            return Response(str(response), mimetype='text/xml')
        
        # Handle the new call
        handle_call_start(call_sid, from_number, to_number)
        
        # Generate TwiML for IVR menu
        response = generate_twiml_response("welcome")
        return Response(str(response), mimetype='text/xml')
    
    except Exception as e:
        logger.error(f"Error handling incoming call: {str(e)}")
        # Return a basic response in case of error
        response = generate_twiml_response("error")
        return Response(str(response), mimetype='text/xml')

@app.route('/handle_ivr', methods=['POST'])
def handle_ivr():
    """Process IVR selection."""
    try:
        digits = request.values.get('Digits', '')
        call_sid = request.values.get('CallSid', 'unknown')
        
        logger.debug(f"IVR selection: {digits} for call {call_sid}")
        
        if digits == '1':
            # Option 1: Play music
            response = generate_twiml_response("music")
            
            # Update call record with choice
            with app.app_context():
                call = Call.query.filter_by(call_sid=call_sid).first()
                if call:
                    call.ivr_selection = "music"
                    db.session.commit()
                    
        elif digits == '2':
            # Option 2: Play beep every 3 seconds
            response = generate_twiml_response("beep")
            
            # Update call record with choice
            with app.app_context():
                call = Call.query.filter_by(call_sid=call_sid).first()
                if call:
                    call.ivr_selection = "beep"
                    db.session.commit()
        else:
            # Invalid option, repeat menu
            response = generate_twiml_response("invalid")
            
        return Response(str(response), mimetype='text/xml')
    
    except Exception as e:
        logger.error(f"Error handling IVR: {str(e)}")
        response = generate_twiml_response("error")
        return Response(str(response), mimetype='text/xml')

@app.route('/call_status', methods=['POST'])
def call_status():
    """Handle call status updates from Twilio."""
    try:
        call_sid = request.values.get('CallSid', 'unknown')
        call_status = request.values.get('CallStatus', 'unknown')
        
        logger.debug(f"Call status update: {call_sid} - {call_status}")
        
        if call_status in ['completed', 'busy', 'failed', 'canceled', 'no-answer']:
            handle_call_end(call_sid)
        
        return jsonify({"status": "success"})
    
    except Exception as e:
        logger.error(f"Error handling call status: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/calls', methods=['GET'])
def api_calls():
    """API endpoint to get active calls."""
    try:
        calls = get_active_calls()
        return jsonify(calls)
    except Exception as e:
        logger.error(f"Error fetching calls: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/call_count', methods=['GET'])
def api_call_count():
    """API endpoint to get current call count."""
    try:
        count = get_call_count()
        return jsonify({"count": count})
    except Exception as e:
        logger.error(f"Error fetching call count: {str(e)}")
        return jsonify({"error": str(e)}), 500

# SSE route for real-time updates
@app.route('/api/stream')
def stream():
    def event_stream():
        previous_count = -1
        while True:
            count = get_call_count()
            calls = get_active_calls()
            
            # Only send updates when there's a change
            if count != previous_count:
                previous_count = count
                data = {
                    "count": count,
                    "calls": calls,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                yield f"data: {json.dumps(data)}\n\n"
            
            time.sleep(1)
    
    return Response(event_stream(), mimetype="text/event-stream")
