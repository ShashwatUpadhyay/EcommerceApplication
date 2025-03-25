from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect
from .models import ContactSubmission
import os
def ContactUs(request):
    try:
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')

            print(name, email, subject, message)

            user = request.user if request.user.is_authenticated else None
            ContactSubmission.objects.create(
                user=user, name=name, email=email, subject=subject, message=message
            )

            if settings.EMAIL_HOST_USER:
                
                try:
                    l = [os.getenv('admin_mail')]
                    print(l)
                    send_mail(
                        subject=f"New Contact Form Submission: {subject}",
                        message=f"""
                        Name: {name}
                        Email: {email}
                        Subject: {subject}
                        Message: {message}
                        """,
                        from_email=email,
                        recipient_list=l, 
                        fail_silently=True,
                    )
                    print()
                except Exception as e:
                    print(f"Error sending email: {e}")

            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')  
    except Exception as e:  
        print(f"Error submitting contact form: {e}")

    return render(request, 'contact.html')
