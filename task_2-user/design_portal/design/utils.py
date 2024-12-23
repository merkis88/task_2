from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from django.utils.http import urlsafe_base64_encode
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """Данный класс генерирует hash по pk от модели Users"""

    def _make_hash_value(self, user, timestamp):
        return (
                str(user.pk) + str(timestamp) + str(user.is_active)
        )


account_activation_token = AccountActivationTokenGenerator()


def send_verification_email(request, user):
    current_site = get_current_site(request).domain
    token = account_activation_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    activation_url = reverse_lazy(
        'confirm_email',
        kwargs={'uidb64': uid, 'token': token}
    )

    subject = "Verify your account - Design.ru"  # Тема письма
    recipient_list = [user.email]  # список получателей

    html_message = render_to_string(
        'registration/email_template.html',
        context={"activate_url": f'http://{current_site}{activation_url}',
                 "image_url": 'https://dogehype.com/public/icon.png'}
    )

    email = EmailMessage(subject=subject,
                         body=html_message,
                         from_email=settings.DEFAULT_FROM_EMAIL,
                         to=recipient_list)
    email.content_subtype = 'html'
    email.send()
