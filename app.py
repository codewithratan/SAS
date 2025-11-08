from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from openpyxl import Workbook
from io import BytesIO
import tempfile
from config import config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Import models here to avoid circular imports
    from models import Customer, ServiceRequest
    from forms import CustomerForm, ServiceRequestForm
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Routes
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/customer/new', methods=['GET', 'POST'])
    def new_customer():
        form = CustomerForm()
        if form.validate_on_submit():
            customer = Customer(
                name=form.name.data,
                contact_number=form.contact_number.data,
                email=form.email.data,
                address=form.address.data
            )
            db.session.add(customer)
            db.session.commit()
            flash('Customer added successfully!', 'success')
            return redirect(url_for('new_service_request', customer_id=customer.id))
        return render_template('customer_form.html', title='New Customer', form=form)
    
    @app.route('/service/new', methods=['GET', 'POST'])
    def new_service_request():
        form = ServiceRequestForm()
        customer_id = request.args.get('customer_id')
        
        if customer_id:
            form.customer_id.data = customer_id
        
        if form.validate_on_submit():
            service_request = ServiceRequest(
                customer_id=form.customer_id.data,
                brand=form.brand.data,
                model_name=form.model_name.data,
                imei_number=form.imei_number.data,
                problem_description=form.problem_description.data,
                warranty_status=form.warranty_status.data,
                device_condition=form.device_condition.data,
                estimate=float(form.estimate.data) if form.estimate.data else None,
                remarks=form.remarks.data,
                notes=form.notes.data
            )
            db.session.add(service_request)
            db.session.commit()
            flash('Service request created successfully!', 'success')
            return redirect(url_for('view_service_request', request_id=service_request.id))
            
        return render_template('service_form.html', 
                             title='New Service Request', 
                             form=form,
                             customer_id=customer_id)
    
    @app.route('/service/<int:request_id>')
    def view_service_request(request_id):
        service_request = ServiceRequest.query.get_or_404(request_id)
        return render_template('service_view.html', service=service_request)
    
    @app.route('/service/<int:request_id>/pdf')
    def generate_pdf(request_id):
        service_request = ServiceRequest.query.get_or_404(request_id)
        
        # Create a file-like buffer to receive PDF data
        buffer = BytesIO()
        
        # Create the PDF object, using the buffer as its "file."
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=72)
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Add some styles
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Center', alignment=1))
        styles.add(ParagraphStyle(name='Right', alignment=2))
        
        # Add header
        elements.append(Paragraph("HARKRISHAN GALLERY AND SERVICES", styles['Title']))
        elements.append(Paragraph("Service Job Card", styles['Heading1']))
        elements.append(Spacer(1, 12))
        
        # Add customer and device information
        customer_info = [
            ['Customer Name:', service_request.customer.name],
            ['Contact Number:', service_request.customer.contact_number],
            ['Address:', service_request.customer.address or 'N/A'],
            ['Email:', service_request.customer.email or 'N/A'],
            ['Date:', service_request.date_received.strftime('%Y-%m-%d %H:%M')],
            ['Job Card #:', f'HGS-{service_request.id:05d}']
        ]
        
        device_info = [
            ['Brand:', service_request.brand],
            ['Model:', service_request.model_name],
            ['IMEI:', service_request.imei_number or 'N/A'],
            ['Warranty:', service_request.warranty_status],
            ['Condition:', service_request.device_condition or 'N/A'],
            ['Estimate:', f'₹{service_request.estimate:.2f}' if service_request.estimate else 'N/A']
        ]
        
        # Create tables for customer and device info
        info_table = Table([
            [
                Table(customer_info, colWidths=[2*inch, 4*inch]),
                Table(device_info, colWidths=[1.5*inch, 4.5*inch])
            ]
        ], colWidths=[6*inch, 6*inch])
        
        info_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ]))
        
        elements.append(info_table)
        elements.append(Spacer(1, 12))
        
        # Add problem description
        elements.append(Paragraph('Problem Description:', styles['Heading3']))
        elements.append(Paragraph(service_request.problem_description, styles['Normal']))
        elements.append(Spacer(1, 12))
        
        # Add remarks and notes if available
        if service_request.remarks:
            elements.append(Paragraph('Remarks:', styles['Heading3']))
            elements.append(Paragraph(service_request.remarks, styles['Normal']))
            elements.append(Spacer(1, 12))
            
        if service_request.notes:
            elements.append(Paragraph('Internal Notes:', styles['Heading3']))
            elements.append(Paragraph(service_request.notes, styles['Normal']))
            elements.append(Spacer(1, 12))
        
        # Add footer
        elements.append(Spacer(1, 24))
        elements.append(Paragraph("Thank you for choosing Harkrishan Gallery and Services", styles['Italic']))
        elements.append(Paragraph("Contact: [Your Contact Info]", styles['Italic']))
        
        # Build the PDF
        doc.build(elements)
        
        # File response
        buffer.seek(0)
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f'hgs_jobcard_{service_request.id}.pdf',
            mimetype='application/pdf'
        )
    
    @app.route('/export/excel')
    def export_to_excel():
        # Create a workbook and add a worksheet
        wb = Workbook()
        ws = wb.active
        ws.title = "Service Requests"
        
        # Add headers
        headers = [
            'Job ID', 'Date', 'Customer Name', 'Contact', 'Brand', 'Model', 
            'IMEI', 'Problem', 'Warranty', 'Estimate', 'Status'
        ]
        ws.append(headers)
        
        # Get all service requests
        service_requests = ServiceRequest.query.join(Customer).all()
        
        # Add data rows
        for sr in service_requests:
            ws.append([
                sr.id,
                sr.date_received.strftime('%Y-%m-%d'),
                sr.customer.name,
                sr.customer.contact_number,
                sr.brand,
                sr.model_name,
                sr.imei_number or '',
                sr.problem_description[:50] + ('...' if len(sr.problem_description) > 50 else ''),
                sr.warranty_status,
                sr.estimate or 0,
                sr.status
            ])
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
            wb.save(tmp.name)
            tmp.seek(0)
            
            return send_file(
                tmp.name,
                as_attachment=True,
                download_name=f'service_requests_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx',
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
    
    @app.route('/search')
    def search():
        query = request.args.get('q', '')
        if not query:
            return render_template('search.html', results=None)
            
        # Search in customers and service requests
        customers = Customer.query.filter(
            (Customer.name.ilike(f'%{query}%')) | 
            (Customer.contact_number.ilike(f'%{query}%')) |
            (Customer.email.ilike(f'%{query}%'))
        ).all()
        
        service_requests = ServiceRequest.query.join(Customer).filter(
            (ServiceRequest.brand.ilike(f'%{query}%')) |
            (ServiceRequest.model_name.ilike(f'%{query}%')) |
            (ServiceRequest.imei_number.ilike(f'%{query}%')) |
            (Customer.name.ilike(f'%{query}%')) |
            (Customer.contact_number.ilike(f'%{query}%'))
        ).all()
        
        return render_template(
            'search.html',
            query=query,
            customers=customers,
            service_requests=service_requests
        )
    
    return app

# For development
if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True)
