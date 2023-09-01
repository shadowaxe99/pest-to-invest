import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os


class EmailManager:
        
        def __init__(self) -> None:
             
            self.smtp_port = 587
            self.sender_email = 'your_email@example.com'
            self.sender_password = 'your_password'

        

        def send_email(self, msg, subject, to, cc, body, date=None, attachments=None):
            msg['From'] = self.sender_email
            msg['To'] = ', '.join(to)
            msg['Cc'] = ', '.join(cc)
            msg['Subject'] = subject

            if date:
                msg['Date'] = date

            msg.attach(MIMEText(body, 'plain'))
            if attachments:
                for attachment in attachments:
                    with open(attachment, 'rb') as file:
                        part.set_payload(file.read())
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment)}')
                        msg.attach(part)

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
