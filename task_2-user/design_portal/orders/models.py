from django.contrib.auth import get_user_model
from django.db import models


class Order(models.Model):
    class ChoicesStatus(models.TextChoices):
        NEW = 'Новая', "NEW"
        ACCEPT = 'Принято', 'ACCEPT'
        DONE = 'Выполнено', 'DONE'

    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=ChoicesStatus.choices,
                              default=ChoicesStatus.NEW, verbose_name='Статус заказа')
    photo = models.ImageField('Изображение категории', upload_to='image/', default=None, null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    objects = models.Manager()

    def __str__(self):
        return self.user.username  # type: ignore

    class Meta:
        verbose_name = 'Заказы'
        verbose_name_plural = 'Заказы'
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]
