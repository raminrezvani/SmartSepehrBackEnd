import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

import after_response
from django.conf import settings
from django.template.loader import render_to_string

from app_admin.models import SocialMedia


@after_response.enable
def send_newsletter_message(subject: str, message: str, direction: int, email: list):
    template_name = "mail_template.html"
    site_front_url = "https://google.com/"

    context = {
        "SUBJECT": subject,
        "MESSAGE": message,
        "SITE_URL": site_front_url if direction == 1 else site_front_url + 'en',
        "LOGO": "https://admin.petrotarh.com/static/image/petrotarh-large-color.png",
        "COMPANY": "پترو طرح" if direction == 1 else "Petrotarh",
        "DIRECTION": "rtl" if direction == 1 else "ltr",
        "LANG": "fa" if direction == 1 else "en",
        "SOCIAL_MEDIA": SocialMedia.objects.filter(soft_delete=False),
        "IMAGE_URL": "https://demo.taefperfumes.com/",
    }
    html = render_to_string(template_name, context=context)

    sender_email = settings.DEFAULT_FROM_EMAIL
    receiver_email = email
    subject = subject

    # Create message object instance
    message = MIMEMultipart()
    message['From'] = formataddr((str(Header(settings.EMAIL_FROM_NAME, 'utf-8')), sender_email))
    message['Subject'] = subject
    message.attach(MIMEText(html, 'html'))

    # SMTP server details
    smtp_server = settings.EMAIL_HOST
    smtp_port = 587
    smtp_username = sender_email
    smtp_password = settings.EMAIL_HOST_PASSWORD

    # Create SMTP session
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    # Login to SMTP server
    server.login(smtp_username, smtp_password)

    # Send email
    for email in receiver_email:
        del message['To']
        message['To'] = email
        server.sendmail(from_addr=sender_email, to_addrs=email, msg=message.as_string())
    # Terminate SMTP session
    server.quit()
