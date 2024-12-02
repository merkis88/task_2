from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings

def send_activation_email(user, request):
    """
    Отправляет письмо с ссылкой для активации учетной записи.
    """
    token = default_token_generator.make_token(user)
    uid = user.pk

    activation_url = request.build_absolute_uri(
        reverse('activate', kwargs={'uid': uid, 'token': token})
    )

    subject = 'Подтверждение вашей регистрации'
    message = f"""
    Привет, {user.username}!

    Спасибо за регистрацию. Перейдите по ссылке ниже, чтобы активировать свою учетную запись:
    {activation_url}

    Если вы не регистрировались, проигнорируйте это письмо.
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, [user.email])
