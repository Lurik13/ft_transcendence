import pyotp
import qrcode
from io import BytesIO
from datetime import datetime, timedelta
import base64

def send_otp(request, use_qr=False):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp_url = totp.provisioning_uri(request.user.email, issuer_name="pong")
    request.session['otp_secret_key'] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=1)
    request.session['otp_valid_date'] = str(valid_date)
    
    if use_qr:
        # Generate a QR code from the provisioning URI
        qr = qrcode.make(otp_url)
        img = BytesIO()
        qr.save(img, format="PNG")
        img.seek(0)
        qr_data = base64.b64encode(img.getvalue()).decode()
        
        return qr_data
    
    print(f"Your one time password is {otp}")
    return None
