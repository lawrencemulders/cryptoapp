import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# SMTP server details
smtp_server = 'your_smtp_server'
smtp_port = 587  # Use the appropriate port for your SMTP server

# SMTP credentials (if required)
smtp_username = 'your_username'
smtp_password = 'your_password'

# Sender and recipient email addresses
sender_email = 'your_email@example.com'
recipient_email = 'recipient@example.com'

# Create a message object
message = MIMEMultipart()
message['From'] = sender_email
message['To'] = recipient_email
message['Subject'] = 'Subject of the email'

# Attach the body of the email
body = 'Body of the email'
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
