from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def send_activation_email(sender, instance, created, **kwargs):
    """
    Отправка письма с подтверждением регистрации
    """
    if created and not instance.is_active:
        token = instance.activation_token  # получаем токен активации
        activation_url = f'{settings.SITE_URL}/activate/{token}/'
        send_mail(
            'Подтверждение регистрации',
            f'Для активации вашей учетной записи, пожалуйста, перейдите по следующей ссылке: {activation_url}',
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False,
        )
