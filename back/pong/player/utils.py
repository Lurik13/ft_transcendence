import pyotp
import qrcode
from io import BytesIO
from datetime import datetime, timedelta
import base64

def create_otp_code(request):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp_url = totp.provisioning_uri(request.user.email, issuer_name="pong")
    request.session['otp_secret_key'] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=2)
    request.session['otp_valid_date'] = str(valid_date)

def send_otp(request, totp, method='email'):
    otp = totp.now()
    # Implement your logic to send OTP via SMS or email
    if method == 'sms':
        # Send OTP via SMS
        pass
    elif method == 'email':
        # Send OTP via email
        pass
    print(f"Your one time password is {otp}")


def create_qr_code(request, totp):
    otp_url = totp.provisioning_uri(request.user.email, issuer_name="pong")
    qr = qrcode.make(otp_url)
    img = BytesIO()
    qr.save(img, format="PNG")
    img.seek(0)
    qr_data = base64.b64encode(img.getvalue()).decode()
    return qr_data