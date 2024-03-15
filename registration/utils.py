from django.core.mail import send_mail
from django.conf import settings
import random
from .models import User


def send_login_email(email):
    subject = "Your account verification OTP...."
    # otp = random.randint(100100,999999)
    otp = 123456
    message = f"Your OTP for account verification is {otp}"
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email])
    user_object = User.objects.get(email= email)
    user_object.otp = otp
    user_object.save()


def send_pass_change_email(email):
    subject = "Your account verification OTP...."
    # otp = random.randint(100100,999999)
    otp = 123456
    message = f"Your OTP for account verification is {otp}"
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email])
    user_object = User.objects.get(email= email)
    user_object.otp = otp
    user_object.is_verified = False
    user_object.save()