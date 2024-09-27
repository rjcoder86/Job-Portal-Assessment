from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator


def send_verification_email(user, request):
    """
    Send a verification email to the user for account activation.

    This function generates a unique token and a user ID, creates an activation link, 
    and sends an email to the user with the activation link to verify their email address.

    Parameters:
    user (User): The user instance for whom the verification email is to be sent.
    request (HttpRequest): The HTTP request object to retrieve the current site's domain.

    Returns:
    None
    """
    try:
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        domain = get_current_site(request).domain
        link = reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
        activate_url = f'http://{domain}{link}'
        email_subject = 'Activate your account'
        email_body = f'Hi {user.first_name}, please use this link to verify your email:\n{activate_url}'
        send_mail(
        email_subject,
        email_body,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )
    except Exception as e:
        print(str(e))

def send_reset_password_email(user, request):
    """
    Send a password reset email to the user.

    This function generates a unique token and a user ID, creates a password reset link, 
    and sends an email to the user with the reset link to allow them to change their password.

    Parameters:
    user (User): The user instance for whom the password reset email is to be sent.
    request (HttpRequest): The HTTP request object to build the absolute URI for the reset link.

    Returns:
    None
    """
    try:
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))

        print(reset_link)
        send_mail(
            'Password Reset Request',
            f'Click the link to reset your password: {reset_link}',
            'your_email@example.com',
            [user.email],
            fail_silently=False,
                    )
    except Exception as e:
        print(str(e))
