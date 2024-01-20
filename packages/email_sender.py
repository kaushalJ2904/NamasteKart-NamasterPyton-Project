# order_processing/email_sender.py
import smtplib
from datetime import datetime

def send_validation_email(total_files, successful_files, rejected_files):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'kj.python.learning@gmail.com'

    #Will disable this password(gamil 2factor authentication) after project evaluation
    #If I comment out this password the entire script will fail
    smtp_password = 'yzjh nraf kfky ucdc'

    business_email = 'kaushaljoshi100@gmail.com'

    subject = f"Validation Email {datetime.today().strftime('%Y-%m-%d')}"
    body = f"Total {total_files} incoming files, {successful_files} successful files, and {rejected_files} rejected files for today."

    # Create the email message
    message = f"Subject: {subject}\n\n{body}"

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)

        server.sendmail(smtp_username, business_email, message)

    print('Validation mail sent')
