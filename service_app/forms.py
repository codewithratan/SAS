from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, SelectField, SubmitField, DateField
from wtforms.validators import DataRequired, Optional, Email, Length
from datetime import datetime

class CustomerForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    contact_number = StringField('Contact Number', validators=[DataRequired(), Length(min=10, max=15)])
    email = StringField('Email', validators=[Optional(), Email()])
    address = TextAreaField('Address')
    submit = SubmitField('Save Customer')

class ServiceRequestForm(FlaskForm):
    customer_id = StringField('Customer ID', validators=[DataRequired()])
    brand = StringField('Brand', validators=[DataRequired()])
    model_name = StringField('Model Name', validators=[DataRequired()])
    imei_number = StringField('IMEI Number', validators=[Optional()])
    problem_description = TextAreaField('Problem Description', validators=[DataRequired()])
    warranty_status = SelectField('Warranty Status', 
                                choices=[
                                    ('', 'Select Warranty Status'),
                                    ('In Warranty', 'In Warranty'),
                                    ('Out of Warranty', 'Out of Warranty'),
                                    ('Extended Warranty', 'Extended Warranty')
                                ], 
                                validators=[DataRequired()])
    device_condition = TextAreaField('Device Condition', validators=[Optional()])
    estimate = DecimalField('Estimated Cost', places=2, validators=[Optional()])
    remarks = TextAreaField('Remarks', validators=[Optional()])
    notes = TextAreaField('Internal Notes', validators=[Optional()])
    submit = SubmitField('Create Service Request')
