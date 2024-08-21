import pyotp
import qrcode
from io import BytesIO
from datetime import datetime, timedelta
import base64
import vonage
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings
from django.shortcuts import get_object_or_404
from .models import Player

import json
from django.core.exceptions import ImproperlyConfigured

with open("secrets.json") as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        raise ImproperlyConfigured(f"Set the {setting} environment variable.")

def create_otp_code(request):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=120)
    otp_url = totp.provisioning_uri(request.user.email, issuer_name="pong")
    request.session['otp_secret_key'] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=2)
    request.session['otp_valid_date'] = str(valid_date)

def send_otp(request, totp, method):

    otp = totp.now()
    print(f"Your one time password is {otp}")
    # Implement your logic to send OTP via SMS or email
    if method == 'sms':
        # Send OTP via SMS
        client = vonage.Client(key=settings.VONAGE_API_KEY, secret=settings.VONAGE_SECRET_KEY)
        sms = vonage.Sms(client)
        responseData = sms.send_message(
        {
            "from": "Vonage APIs",
            "to": "+33628096286", #request.user.phone_number
            "text": f"Your one time password is {otp}\n",
        })
        if responseData["messages"][0]["status"] == "0":
            print("Message sent successfully.")
        else:
            print(f"Message failed with error: {responseData['messages'][0]['error-text']}")

    elif method == 'email':
        # Email details
        sender_email = settings.SMTP_USERNAME
        receiver_email = "alex.derouineau@live.fr" #request.user.email
        subject = "PONG Verification Code"
        body = f"Your Verification code is : {otp}"

        
        # SMTP Server Configuration
        smtp_server = settings.SMTP_SERVER
        smtp_port = settings.SMTP_PORT
        smtp_username = settings.SMTP_USERNAME
        smtp_password = settings.SMTP_PASSWORD

        print(f"smtp_server: {smtp_server}")
        print(f"smtp_port: {smtp_port}")
        print(f"smtp_username: {smtp_username}")
        print(f"smtp_password: {smtp_password}")

        # SMTP Server Configuration
        #SMTP_SERVER = "127.0.0.1"
        #SMTP_PORT = 1025
        #SMTP_USERNAME = "proj42_lh@proton.me"
        #SMTP_PASSWORD = get_secret('smtp_password')

        # Create the email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.login(smtp_username, smtp_password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
                print("Email sent successfully.")
        except Exception as e:
            print(f"Failed to send email: {e}")

def create_qr_code(request, totp):
    otp_url = totp.provisioning_uri(request.user.email, issuer_name="pong")
    qr = qrcode.make(otp_url)
    img = BytesIO()
    qr.save(img, format="PNG")
    img.seek(0)
    qr_data = base64.b64encode(img.getvalue()).decode()
    return qr_data