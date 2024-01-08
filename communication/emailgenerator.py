import smtplib
import time
import schedule
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta


# SMTP server details
smtp_server = 'smtp.gmail.com'
smtp_port = 587  # Use the appropriate port for your SMTP server

# SMTP credentials (if required)
smtp_username = 'astrowealth975@gmail.com'
smtp_password = ''

sender_email = 'astrowealth975@gmail.com'

def send_email(recipient_email):
    # Create a message object
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = 'CryptoApp: Movement Update'

    # Attach the body of the email
    body = 'This is a test written in python code'
    message.attach(MIMEText(body, 'plain'))

    # Create an SMTP session
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # Login to the SMTP server (if required)
            server.starttls()  # Use this line for a secure connection
            server.login(smtp_username, smtp_password)

            # Send the email
            server.sendmail(sender_email, recipient_email, message.as_string())

        print('Email sent successfully!')
    except Exception as e:
        print(f'Error sending email: {e}')

def send_scheduled_email():
    # Sender and recipient email addresses
    recipient_email = 'test@hotmail.com'

    # Create a message object
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = 'CryptoApp: Movement Update'

    # Attach the body of the email
    body = 'This is a test written in Python code'
    message.attach(MIMEText(body, 'plain'))

    # Create an SMTP session
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # Login to the SMTP server (if required)
            server.starttls()  # Use this line for a secure connection
            server.login(smtp_username, smtp_password)

            # Send the email
            server.sendmail(sender_email, recipient_email, message.as_string())

        print('Email sent successfully!')
        schedule.every().sunday.at('12:00').do(send_scheduled_email)
        while True:
            schedule.run_pending()
            time.sleep(1)
    except Exception as e:
        print(f'Error sending email: {e}')
