import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd

def read_results_data(file_path):
    data = pd.read_csv(file_path)
    return data

def generate_email_content(name, subject_marks,percentage,Final_result):
    # HTML header and footer
    html_header = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Exam Results Header</title>
        <style>
            body {
                margin: 0;
                padding: 0;
                background-color: #f8f8f8;
                font-family: 'Arial', sans-serif;
            }

            .header {
                background-color: #3498db;
                color: #fff;
                text-align: center;
                padding: 10px;
            }

            .header h1 {
                margin: 0;
            }

            .table-container {
                margin: 20px;
            }

            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }

            table, th, td {
                border: 1px solid #ddd;
            }

            th, td {
                padding: 10px;
                text-align: left;
            }

            th {
                background-color: #3498db;
                color: #fff;
            }
          .result-info {
                text-align: center;
                margin-top: 20px;
                margin-left: auto; 
                margin-right: 10px;
                }

            .footer {
                text-align: center;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Exam Results</h1>
            <p>Dear """ + f"{name}" +""", here are your exam results:</p>
        </div>

        <div class="table-container">
            <table>
                <tr>
                    <th>Subject</th>
                    <th>Marks</th>
                    <th>result</th>
                </tr>
                """ + f"{subject_marks}" +"""
            </table>
        </div>
         <div class="result-info">
            <p>Your overall percentage is <b>""" + f"{percentage}%" +"""</b></p>
            <p>Final Result  is <b>""" + f"{Final_result}" +"""</b></p>
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

    # Concatenate the HTML components
    email_content = html_header + html_footer
    return email_content

def send_result_email(subject, body, to_email):
    # SMTP configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = '<yourEMail>'
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

# Function to calculate overall percentage
def calculate_percentage(subject_marks):
    total_marks = sum(subject_marks.values())
    total_subjects = len(subject_marks)
    percentage = (total_marks / (total_subjects * 100)) * 100
    return round(percentage, 2)

# Main function to process and send exam result emails
def send_exam_result_emails(file_path):
    results_data = read_results_data(file_path)

    for index, row in results_data.iterrows():
        student_name = row['Student Name']
        student_email = row['Email']

        # Extract subject-wise marks and convert to a dictionary
        subject_marks = {
            'C Programming (T)': row['C Programing(T)'],
            'Java Programming (T)': row['Java Programming(T)'],
            'Digital Electronic (T)': row['Digital Electronic(T)'],
            'C Programming (P)': row['C Programming (P)'],
            'Java Programming (P)': row['Java Programming (P)'],
        }

        # Generate the subject-wise marks table
        result=""
        Final_result=""
        table_rows = ""
        for subject, marks in subject_marks.items():
            if marks>=35:
                result="Pass"
                table_rows += f"<tr><td>{subject}</td><td>{marks}</td><td>{result}</td></tr>"
            else:
                result="Fail"
                Final_result="Fail"
                table_rows += f"<tr><td>{subject}</td><td>{marks}</td><td>{result}</td></tr>"
        # Generate the overall percentage
        overall_percentage = calculate_percentage(subject_marks)
        if Final_result != "Fail":
            if overall_percentage >=80.0:
                Final_result= "Distiction"
            elif overall_percentage >=60:
                Final_result= "First Class"
            elif overall_percentage >=40:
                Final_result= "Second class"
            elif overall_percentage>=35:
                Final_result="Pass"
        else:
            Final_result="Fail"

        # Generate the email content
        email_body = generate_email_content(student_name, table_rows.format(subject_marks), overall_percentage,Final_result)

        # Send the email
        email_subject = "Exam Results Notification"
        send_result_email(email_subject, email_body, student_email)

# Get file path for exam results data
results_file_path = "Exam Results Notification\Student_result.csv"

# Execute the script to send exam result emails
send_exam_result_emails(results_file_path)
print("All students result emails sent successfully ")