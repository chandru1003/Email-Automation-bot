import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import schedule
import time
from datetime import datetime

# Function to read data from CSV or Excel file
def read_data(file_path):
    # Assuming the file contains 'email', 'name', 'dob', and 'message' columns
    data = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)
    return data

# Function to generate HTML email content
def generate_email_content(name, message):
    # HTML header and footer
    html_header = "<html><head></head><body>"
    html_footer = "</body></html>"

    # Combine header, personalized message, and footer
    html_body = f"<p>Dear {name},</p><p>{message}</p>"
    
    # Concatenate the HTML components
    email_content = html_header + html_body + html_footer
    return email_content

# Function to send the email
def send_email(subject, body, to_email):
    # Set up your email configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'your_email@gmail.com'
    smtp_password = 'your_email_password'

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

# Function to check if today is someone's birthday and send emails
def check_and_send_birthday_emails(file_path):
    data = read_data(file_path)
    today = datetime.now().strftime("%m-%d")

    for index, row in data.iterrows():
        dob_month_day = row['DOB'].strftime("%m-%d")
        if dob_month_day == today:
            email_subject = "Automated Email: Happy Birthday!"
            email_body = generate_email_content(row['Name'], row['Message'])
            send_email(email_subject, email_body, row['Email'])

# Get file path for data
file_path = "path/to/your/data.csv"  # Replace with the actual file path

# Schedule and check/send birthday emails every day at a specific time (adjust as needed)
schedule.every().day.at("10:00").do(check_and_send_birthday_emails, file_path)

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
