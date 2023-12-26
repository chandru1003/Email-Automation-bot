import os
import smtplib
import pandas as pd
from datetime import datetime
from email.mime.text import MIMEText
from PyPDF2 import PdfWriter, PdfFileReader
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


# Function to read participant data from CSV
def read_participant_data(file_path):
    return pd.read_csv(file_path)


def replace_placeholders(template_pdf, replacements):
    for page_num in range(len(template_pdf.pages)):
        template_page = template_pdf.pages[page_num]
        content = template_page.extract_text()
        
        for key, value in replacements.items():
            content = content.replace(f"<{key}>", str(value))

        template_page.mergePage(template_page)
    
    return template_pdf

def generate_certificate(template_path, output_folder, participant):
    # Create a PDF document by merging the template with participant details
    output_path = os.path.join(output_folder, f"{participant}_Certificate.pdf")

    with open(template_path, 'rb') as template_file, open(output_path, 'wb') as output_file:
        template_pdf = PdfFileReader(template_file)
        output_pdf_writer = PdfWriter()

        # Replace placeholders in the template
        modified_pdf = replace_placeholders(template_pdf, {
            "name": participant,
            "date": datetime.now().strftime('%Y-%m-%d'),
        })
        print(modified_pdf)
        # Add modified pages to the output PDF
        for page_num in range(modified_pdf.getNumPages()):
            output_pdf_writer.addPage(modified_pdf.getPage(page_num))

        # Save the modified PDF
        output_pdf_writer.write(output_file)

    return output_path

'''
def generate_certificate(template_path, output_folder, participant):
    # Create a PDF document by merging the template with participant details
    output_path = os.path.join(output_folder, f"{participant}_Certificate.pdf")

    with open(template_path, 'rb') as template_file, open(output_path, 'wb') as output_file:
        template_pdf = PdfFileReader(template_file)
        output_pdf = PdfWriter()

        # Copy pages from the template
        for page_num in range(template_pdf.getNumPages()):
            template_page = template_pdf.getPage(page_num)
            output_pdf.addPage(template_page)

        # Create a new canvas to draw on the PDF
        c = canvas.Canvas(output_file)

        # Add participant details to the certificate
        c.drawString(100, 750, f"Certificate of Participation for {participant}")
        c.drawString(100, 730, f"This is to certify that")
        c.drawString(100, 710, f"{participant}")
        c.drawString(100, 690, f"has successfully attended the event.")
        c.drawString(400, 690, f"Date: {datetime.now().strftime('%Y-%m-%d')}")
        # Save the PDF modifications
        c.save()

        # Update the output PDF file with the modified page
        output_pdf_writer = PdfWriter()
        output_pdf_writer.addPage(output_pdf.getPage(page_num))
        output_pdf_writer.write(output_file)

    return output_path
'''
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
def send_email(to_email, body,certificate_path):
    # Set up your email configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'chandrukongari@gmail.com'
    smtp_password = 'nonq qhue mcxe szae'

    # Create the email message
    message = MIMEMultipart()
    message['From'] = smtp_username
    message['To'] = to_email
    message['Subject'] = 'Thanks for Attending!'  
    
    # Attach the certificate PDF to the email
    with open(certificate_path, 'rb') as certificate_file:
        certificate_attachment = MIMEApplication(certificate_file.read(), _subtype="pdf")
        certificate_attachment.add_header('Content-Disposition', f'attachment; filename={participant_name}_Certificate.pdf')
        message.attach(certificate_attachment)
    
    # Attach the HTML body to the email
    message.attach(MIMEText(body, 'html'))
    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, to_email, message.as_string())

# Read participant data from CSV
filePath='Email Certificate Automation\Participants-List.csv'
template_path='Email Certificate Automation\Certificate Template.pdf'
output_folder='Email Certificate Automation\Output certificate'
participant_data = read_participant_data(filePath)

# Iterate through participants and send personalized emails
for index, row in participant_data.iterrows():
    participant_name = row['Name']
    participant_email = row['Email']    
    html_mail=generate_email_content(participant_name)   
    certificate_path = generate_certificate(template_path, output_folder,participant_name)
    send_email(participant_email, html_mail,certificate_path)   

print('Emails sent successfully!')
