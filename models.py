from app import db
from datetime import datetime

class Call(db.Model):
    """Model for storing call information."""
    id = db.Column(db.Integer, primary_key=True)
    call_sid = db.Column(db.String(100), unique=True, nullable=False)
    from_number = db.Column(db.String(50), nullable=False)
    to_number = db.Column(db.String(50), nullable=False)
    ivr_selection = db.Column(db.String(20), nullable=True)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Call {self.call_sid}>'
    
    def to_dict(self):
        """Convert call to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'call_sid': self.call_sid,
            'from_number': self.from_number,
            'to_number': self.to_number,
            'ivr_selection': self.ivr_selection,
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S') if self.start_time else None,
            'end_time': self.end_time.strftime('%Y-%m-%d %H:%M:%S') if self.end_time else None,
            'is_active': self.is_active,
            'duration': (datetime.utcnow() - self.start_time).total_seconds() if self.is_active else None
        }
