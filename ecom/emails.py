from django.core.mail import send_mail
from ecom.settings import DOMAIN_NAME , EMAIL_HOST_USER

def order_successful(order):
    subject = 'Order Successful'
    message = f'Hi {order.user.extra.full_name},\n\nYour order has been placed successfully.\n\nOrder ID: {order.uid}\n\nTotal Amount: {order.cart.final_price}\n\nThank you for shopping with us.\n\nRegards,\n{DOMAIN_NAME}'
    recipient_list = [order.user.email, order.address.email]
    send_mail(subject, message, EMAIL_HOST_USER, recipient_list)