import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
from datetime import datetime

# Function to read data from CSV file
def read_data(file_path):
    data = pd.read_csv(file_path)
    return data

# Function to generate HTML email content
def generate_email_content(name):
    # HTML header and footer
    html_header = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Happy Birthday!</title>
        <style>
            /* Add your custom styles for the header here */
            body {
                margin: 0;
                padding: 0;
                background-color: #f8f8f8;
                font-family: 'Arial', sans-serif;
            }

            .header {
                background-color: #ffcc00;
                color: #fff;
                text-align: center;
                padding: 10px;
            }

            .header h1 {
                margin: 0;
            }

            .body {
                padding: 20px;
            }
        </style>
    </head>
    <body>
        <div class="header">
            """ + f"<h1>Happy Birthday, {name}!</h1>"+ """
        </div>
    """

    html_body = """
        <div class="body">
            """ + f"<p>Dear {name},</p>"  + """
            <p>Wishing you a fantastic birthday filled with joy, laughter, and unforgettable moments!</p>
            <p>May this year bring you all the happiness and success you deserve. Enjoy your special day to the fullest!</p>
            <p>Best regards,</p>
            <p>Your Sender Name</p>
        </div>
    """

    html_footer = """
        <div class="footer">
            <p>Contact us for more information: <a href="mailto:info@example.com">info@example.com</a></p>
            <p>&copy; 2023 Your Company. All rights reserved.</p>
        </div>
    </body>
    </html>
    """

    # Combine header and footer
    email_content = html_header + html_body + html_footer
    return email_content

# Function to send the email
def send_email(subject, body, to_email):
    # Set up your email configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = '<Your email Id>'
    smtp_password = ''

    # Create the email message
    message = MIMEMultipart()
    message['From'] = smtp_username
    message['To'] = to_email
    message['Subject'] = subject

    # Attach the HTML body to the email
    message.attach(MIMEText(body, 'html'))

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, to_email, message.as_string())

# Function to send birthday emails
def send_birthday_emails(file_path):
    data = read_data(file_path)
    today = datetime.now().strftime("%d-%m")

    for index, row in data.iterrows():
        dob_day_month = row['DOB'][0:5]
        if dob_day_month == today:
            email_subject = " Happy Birthday! "+ row['Name']
            email_body = generate_email_content(row['Name'])
            send_email(email_subject, email_body, row['Email'])

# Get file path for data
file_path = "DOB.csv"

# Send birthday emails
send_birthday_emails(file_path)

print("Birthday emails sent successfully!")