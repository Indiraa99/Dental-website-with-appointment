from flask import render_template, redirect, url_for, flash, request
from app import app
import pandas as pd
from datetime import datetime

appointments = [] 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        date = request.form.get('date')
        time = request.form.get('time')
        chief_complaint = request.form.get('chiefComplaint')

        # Validate the data 
        if not all([name, email, phone, date, time,chief_complaint]):
            flash('Please fill in all fields.', 'error')
            return redirect(url_for('booking'))

        # Create a DataFrame to store the appointment data
        new_data = pd.DataFrame({
            'Name': [name],
            'Email': [email],
            'Phone': [phone],
            'Date': [date],
            'Time': [time],
            'Timestamp': [datetime.utcnow()],
            'Chief Complaint': [chief_complaint]
        })

        # Check if the file exists
        file_path = 'appointments.xlsx'
        file_exists = df_exists(file_path)

        # If the file exists, read the existing data and append the new data
        if file_exists:
            existing_data = pd.read_excel(file_path)
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            # If the file doesn't exist, create it with the new data
            updated_data = new_data

        # Write the updated data to the Excel file
        updated_data.to_excel(file_path, index=False)

        # Render a confirmation page with the appointment details
        return render_template('confirmation.html', appointment={
            'name': name,
            'email': email,
            'phone': phone,
            'date': date,
            'time': time,
            'chief_complaint': chief_complaint
        })
        flash('Appointment booked successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('booking.html')

def df_exists(file_path):
    try:
        pd.read_excel(file_path)
        return True
    except FileNotFoundError:
        return False
