import pyotp
import qrcode
from io import BytesIO
from datetime import datetime, timedelta
import base64
import vonage
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
        client = vonage.Client(key="afd3aa42", secret="iVfgXrRleEydLwA0")
        sms = vonage.Sms(client)
        responseData = sms.send_message(
        {
            "from": "Vonage APIs",
            "to": "+33628096286",
            "text": f"Your one time password is {otp}\n",
        })
        if responseData["messages"][0]["status"] == "0":
            print("Message sent successfully.")
        else:
            print(f"Message failed with error: {responseData['messages'][0]['error-text']}")

    elif method == 'email':
        # Email details
        sender_email = "proj42_lh@proton.me"
        receiver_email = "alex.derouineau@live.fr"
        subject = "PONG Verification Code"
        body = f"Your Verification code is : {otp}"

        # SMTP Server Configuration
        smtp_server = "127.0.0.1"
        smtp_port = 1025
        smtp_username = "proj42_lh@proton.me"
        smtp_password = "lLMUAPhtJS-5PlaAOJfAnQ"

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