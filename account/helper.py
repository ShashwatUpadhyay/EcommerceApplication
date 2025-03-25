from django.core.mail import send_mail
import uuid
from django.conf import settings
from django.contrib.auth.models import User
from ecom.settings import DOMAIN_NAME
def send_forget_password_email(email, token):
    token = token
    subject = 'Forget Password link'
    html_message = f'Click on the link to reset your password {DOMAIN_NAME}user/password-reset-confirm/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    fail_silently = False
    send_mail( subject,fail_silently, email_from, recipient_list , html_message=html_message)
    return True

# def contact_submission(email):
#     subject = 'Feedback & Support'
#     message = f'Your password has been changed successfully. If you did not change your password then contact us immediately.'
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = [email]
#     send_mail( subject, message, email_from, recipient_list )
#     return True