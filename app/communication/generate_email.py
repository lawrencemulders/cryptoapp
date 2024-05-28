import os
import smtplib
import time
import schedule
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from queue_handling import AutoRemoveQueue


# Load environment variables from .env file
load_dotenv()

# SMTP server details
smtp_server = 'smtp.gmail.com'
smtp_port = 587  # Use the appropriate port for SMTP server

# SMTP credentials

smtp_username = os.getenv("SMTPUSERNAME")
# TO DO: convert to method
if smtp_username is None:
    raise KeyError(f"{smtp_username} environment variable is not set. Please check your .env file.")
smtp_password = os.getenv("SMTPPASSWORD")

sender_email = os.getenv("SMTPUSERNAME")
recipient_email = os.getenv("RECIPIENTEMAIL")

# Allow only 1 item pending in queue
scheduled_email_queue = AutoRemoveQueue(maxsize=1)


def send_email(table):

    # Create a message object
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = 'CryptoApp: Movement Update'

    html_table = table.get_html_string(attributes={"border": "1"})
    html_content = f"""
    <html>
    <head>
    <style>
      table, th, td {{
        border: 1px solid black;
        border-collapse: collapse;
      }}
      th, td {{
        padding: 8px;
        text-align: left;
      }}
      tr:nth-child(even) {{
        background-color: #f2f2f2;
      }}
      th {{
        background-color: #4CAF50;
        color: white;
      }}
    </style>
    </head>
    <body>
    This email has been generated with Python 3.11 code. 
    See the following results to view your portfolio's performance.
    {html_table}
    </body>
    </html>
    """

    message.attach(MIMEText(html_content, 'html'))

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


def send_scheduled_email(table):

    # Load environment variables from .env file
    load_dotenv()

    schedule_time = os.getenv("SCHEDULE_TIME")
    schedule_day = os.getenv("SCHEDULE_DAY")

    # Create a message object
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = 'CryptoApp: Movement Update'

    html_table = table.get_html_string(attributes={"border": "1"})
    html_content = f"""
    <html>
    <head>
    <style>
      table, th, td {{
        border: 1px solid black;
        border-collapse: collapse;
      }}
      th, td {{
        padding: 8px;
        text-align: left;
      }}
      tr:nth-child(even) {{
        background-color: #f2f2f2;
      }}
      th {{
        background-color: #4CAF50;
        color: white;
      }}
    </style>
    </head>
    <body>
    This email has been generated with Python 3.11 code. 
    See the following results to view your portfolio's performance.
    {html_table}
    </body>
    </html>
    """

    message.attach(MIMEText(html_content, 'html'))

    # Create an SMTP session
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # Login to the SMTP server (if required)
            server.starttls()  # Use this line for a secure connection
            server.login(smtp_username, smtp_password)

            # Send the email
            server.sendmail(sender_email, recipient_email, message.as_string())

        print('Email sent successfully!')
    except smtplib.SMTPException as e:
        print(f"Error sending email to {recipient_email}: {e}")
        # Enqueue the email task to be retried later
        scheduled_email_queue.put(table)

    getattr(schedule.every(), schedule_day).at(schedule_time).do(send_scheduled_email)

    # Main loop to process the email queue and check scheduled tasks
    while True:
        # Check if there are scheduled email tasks in the queue
        while not scheduled_email_queue.empty():
            table = scheduled_email_queue.get()
            send_scheduled_email(table)
            # Add a delay before resending email if no connection
            time.sleep(3600)  # 1-hour delay
        schedule.run_pending()
        time.sleep(1)
