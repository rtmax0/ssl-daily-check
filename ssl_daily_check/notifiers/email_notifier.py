import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .base import BaseNotifier

class EmailNotifier(BaseNotifier):
    def __init__(self, smtp_server, smtp_port, sender_email, sender_password, recipient_email):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.recipient_email = recipient_email

    def send_notification(self, expired_domains):
        subject = "SSL证书过期提醒"
        message = "以下域名的SSL证书即将过期:\n\n"
        for domain, description, days in expired_domains:
            message += f"- {domain} ({description}): {days}天后过期\n"

        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = self.recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            print("邮件发送成功")
        except Exception as e:
            print(f"邮件发送失败: {str(e)}")
