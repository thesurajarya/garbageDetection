from app import db
from datetime import datetime

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    issue_type = db.Column(db.String(50))
    location = db.Column(db.String(255))
    image_path = db.Column(db.String(255))
    status = db.Column(db.String(20), default="Pending")
    is_valid_garbage = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
