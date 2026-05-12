import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import sqlite3


def send_email(to_email, medicine_name, dosage):
    sender_email = "your_email@gmail.com"
    sender_password = "your_app_password"

    subject = "Medication Reminder 💊"
    body = f"""
    Time to take your medicine!

    Medicine: {medicine_name}
    Dosage: {dosage}

    Stay healthy ❤️
    """

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.send_message(msg)
    server.quit()