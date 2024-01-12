import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import pyotp


class MailOTP:
    otp_storage = {}

    @staticmethod
    def send_email(to_email, subject, body, attachment=None):
        from app import app
        from_email = app.config['MAIL_USERNAME']

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        if attachment:
            with open(attachment, 'rb') as file:
                part = MIMEApplication(file.read(), Name="attachment.pdf")
                part['Content-Disposition'] = 'attachment; filename="attachment.pdf"'
                msg.attach(part)

        with smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT']) as server:
            server.starttls()
            server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            server.sendmail(from_email, to_email, msg.as_string())

    def send_otp(self, email):
        from app import app
        # Tạo mã OTP
        totp = pyotp.TOTP(app.config['MAIL_SECRET_KEY'])
        otp = totp.now()

        # Lưu trữ mã OTP cho người dùng (trong thực tế, sử dụng cơ sở dữ liệu để lưu trữ)
        self.otp_storage[email] = otp

        # Gửi mã OTP qua email
        subject = "Your One-Time Password"
        body = f"Your OTP is: {otp}"
        self.send_email(email, subject, body)

    def verify_otp(self, email, otp):
        # Lấy mã OTP đã lưu trữ cho người dùng
        stored_otp = self.otp_storage.get(email)

        try:
            otp = int(otp)
            stored_otp = int(stored_otp)
        except Exception as e:
            print(e)
            return False

        # Kiểm tra mã OTP
        if stored_otp and otp == stored_otp:
            return True
        else:
            return False
