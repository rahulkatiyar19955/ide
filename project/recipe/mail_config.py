import smtplib
from email.mime.text import MIMEText
import pyotp
import os

timeotp = pyotp.TOTP('base32secret3232', interval=120)

smtp_ssl_host = 'smtp.gmail.com'
smtp_ssl_port = 465

username = os.environ.get("username")
password = os.environ.get("password")
# print(username,password)
sender = 'Rahul'


# targets = ['rahulkatiyar19955@gmail.com']


def send_mail(rec, msg1, sender='Coding IDE', subject='Coding IDE'):
    msg = MIMEText(msg1)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = rec

    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    server.login(username, password)
    server.sendmail(sender, rec, msg.as_string())
    server.quit()


def send_otp(rec):
    print("send otp:",rec)
    user_otp = get_otp()
    msg = 'Hi, Thankyou for registration.' + '\npassword: ' + user_otp
    send_mail(rec=rec, sender='Coding IDE', msg1=msg)


def get_otp():
    return timeotp.now()


def check_otp(pass_key: str):
    if timeotp.verify(pass_key):
        return True
    else:
        return False
