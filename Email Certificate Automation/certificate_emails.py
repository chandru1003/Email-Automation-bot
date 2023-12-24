import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import pandas as pd
from reportlab.pdfgen import canvas
from datetime import datetime

# Function to read participant data from CSV
def read_participant_data(file_path):
    return pd.read_csv(file_path)


# Function to send an email with certificate attachment
def send_email(to_email, participant_name):
    # Set up your email configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'chandrukongari@gmail.com'
    smtp_password = 'pchb hgym fowb pdbf'

    # Create the email message
    message = MIMEMultipart()
    message['From'] = smtp_username
    message['To'] = to_email
    message['Subject'] = 'Thanks for Attending!'

    # Email body
    email_body = f"""
    Dear {participant_name},

    Thank you for attending our event! We appreciate your participation.

    Attached to this email is your Certificate of Participation.

    Best regards,
    Your Organization
    """

    # Attach the email body
    message.attach(MIMEText(email_body, 'plain'))

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, to_email, message.as_string())

# Read participant data from CSV
filePath='Email Certificate Automation\Participants-List.csv'
participant_data = read_participant_data(filePath)

# Iterate through participants and send personalized emails
for index, row in participant_data.iterrows():
    participant_name = row['Name']
    participant_email = row['Email']
    
    
    
    # Send an email with the certificate attachment
    send_email(participant_email, participant_name)

   

print('Emails sent successfully!')
