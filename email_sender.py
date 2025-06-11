import smtplib
from email.message import EmailMessage

def send_email_with_password(recipient_email, password):
    sender_email = "sathvikachsr13@gmail.com"
    sender_password = "ukyh qhwc ywnr trdy"  

    subject = "Password for Secure PDF"
    body = f"""
Hello,

The password to access your secure PDF is:

🔐 {password}

Please do not share this password with anyone else.

Best regards,
SecureQR App
"""

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        return "Success"
    except Exception as e:
        return f"Failed to send email: {str(e)}"

