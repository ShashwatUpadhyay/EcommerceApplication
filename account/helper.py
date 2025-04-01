from django.core.mail import send_mail
import uuid
from django.conf import settings
from django.contrib.auth.models import User
from ecom.settings import DOMAIN_NAME
from django.template.loader import render_to_string
from django.utils.html import strip_tags

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



def send_order_confirmation_email(order):
    subject = f"Order Confirmation - {order.uid}"
    recipient_email = order.user.email  
    from_email = settings.DEFAULT_FROM_EMAIL

    # Create email content using template
    html_message = render_to_string('order_confirmation_email.html', {'order': order})
    plain_message = strip_tags(html_message)  

    # Send email
    send_mail(
        subject,
        plain_message,
        from_email,
        [recipient_email],
        html_message=html_message
    )