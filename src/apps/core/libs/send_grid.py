# Using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
from typing import List
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, \
    FileContent, FileName, FileType, Disposition


class SendGrid:
    API_KEY = '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'
    FROM_EMAIL = 'no-reply@lprs.com'

    @classmethod
    def send_mail(cls, email: List[str], subject: str, html: str,
                  attached_content: bytes = None):
        # TODO: To change mailtrap in to dev env
        # if settings.DEBUG:
        #     from django.core.mail import send_mail
        #
        #     return send_mail(
        #         subject=subject,
        #         html_message=html,
        #         message=html,
        #         from_email=cls.FROM_EMAIL,
        #         recipient_list=email,
        #         fail_silently=False,
        #     )


        message = Mail(
            from_email=cls.FROM_EMAIL,
            to_emails=email,
            subject=subject,
            html_content=html
        )
        sg = SendGridAPIClient(cls.API_KEY)
        try:
            response = sg.send(message)
        except Exception as error:
            print(error)
        else:
            return response
