import os
import base64

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)

class Sendgrid_Email:
    def __init__(self, api_key):
        self.api_key = api_key
    
    def send_email(self, to_email, from_email, file_name):
        message = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject='Worklog at ' + file_name,
            html_content='<strong>Work log at '+file_name+'</strong>'
        )

        with open(file_name, 'rb') as f:
            data = f.read()
            f.close()
        encoded_file = base64.b64encode(data).decode()

        attachedFile = Attachment(
            FileContent(encoded_file),
            FileName(file_name),
            FileType('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
            Disposition('attachment')
        )
        message.attachment = attachedFile

        sg = SendGridAPIClient(self.api_key)
        response = sg.send(message)
        return (response.status_code, response.body, response.headers)