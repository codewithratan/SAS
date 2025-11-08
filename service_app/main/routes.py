from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from service_app.main import bp
from service_app.models import Customer, ServiceRequest
from datetime import datetime, timedelta

@bp.route('/')
@bp.route('/index')
def index():
    # Get recent service requests
    recent_requests = ServiceRequest.query.order_by(
        ServiceRequest.date_received.desc()
    ).limit(5).all()
    
    # Get statistics
    total_customers = Customer.query.count()
    total_services = ServiceRequest.query.count()
    pending_services = ServiceRequest.query.filter_by(status='Pending').count()
    
    return render_template('index.html', 
                         recent_requests=recent_requests,
                         total_customers=total_customers,
                         total_services=total_services,
                         pending_services=pending_services)
