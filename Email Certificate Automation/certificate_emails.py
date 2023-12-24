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

def generate_email_content(name):
    html_body=""" <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Thank You for Attending</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f5f5f5;
            text-align: center;
            margin: 0;
            padding: 0;
        }

        .header {
            background-color: #4CAF50;
            color: #fff;
            padding: 20px;
        }

        .content {
            padding: 20px;
        }

        .gif {
            margin-top: 20px;
        }

        .footer {
            background-color: #4CAF50;
            color: #fff;
            padding: 10px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Thank You for Attending!</h1>
    </div>

    <div class="content">
        <p>Dear"""+ f"{name}"""",</p>
        <p>It was a pleasure having you at our event. Your participation made it truly special.</p>
       
    </div>

 

    <div class="gif">
        <img src="Email Certificate Automation\thankyou.png" alt="Thank You GIF" width="300" height="200">
    </div>

    <div class="footer">
        <p>Thank you again and looking forward to seeing you in future events!</p>
    </div>
</body>
</html>
"""
    return html_body
# Function to send an email with certificate attachment
def send_email(to_email, body):
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
    
    # Attach the HTML body to the email
    message.attach(MIMEText(body, 'html'))
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
    html_mail=generate_email_content(participant_name)   
    send_email(participant_email, html_mail)

   

print('Emails sent successfully!')
