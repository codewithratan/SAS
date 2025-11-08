from datetime import datetime
from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    address = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    services = db.relationship('ServiceRequest', backref='customer', lazy=True)

    def __repr__(self):
        return f"Customer('{self.name}', '{self.contact_number}')"

class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    model_name = db.Column(db.String(100), nullable=False)
    imei_number = db.Column(db.String(20), nullable=True)
    problem_description = db.Column(db.Text, nullable=False)
    warranty_status = db.Column(db.String(20), nullable=False)  # In Warranty, Out of Warranty, etc.
    device_condition = db.Column(db.Text, nullable=True)
    estimate = db.Column(db.Float, nullable=True)
    remarks = db.Column(db.Text, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='Pending')  # Pending, In Progress, Completed, Delivered
    date_received = db.Column(db.DateTime, default=datetime.utcnow)
    date_completed = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f"ServiceRequest('{self.brand} {self.model_name}', '{self.status}')"
