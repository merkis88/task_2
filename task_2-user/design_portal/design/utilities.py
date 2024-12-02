from django.template.loader import render_to_string
from django.core.signing import Signer
from django.core.mail import send_mail
from django.conf import settings

signer = Signer()


def send_activation_notification(user):
    """
    Отправляет письмо с активацией для нового пользователя.
    """
    host = f"http://{settings.ALLOWED_HOSTS[0]}" if settings.ALLOWED_HOSTS else "http://localhost:8000"

    context = {
        'user': user,
        'host': host,
        'sign': signer.sign(user.username),
    }

    subject = render_to_string('email/activation_letter_subject.txt', context).strip()
    body_text = render_to_string('email/activation_letter_body.txt', context)

    send_mail(
        subject=subject,
        message=body_text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
