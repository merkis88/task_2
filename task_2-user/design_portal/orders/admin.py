from django.contrib import admin
from .models import Order


@admin.action(description="Сменить статус на 'Принято'")
def mark_as_accepted(modeladmin, request, queryset):
    queryset.update(status=Order.ChoicesStatus.ACCEPT)


@admin.action(description="Сменить статус на 'Выполнено'")
def mark_as_done(modeladmin, request, queryset):
    queryset.update(status=Order.ChoicesStatus.DONE)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'time_create')  # Поля для отображения
    list_filter = ('status', 'time_create')  # Фильтрация
    actions = [mark_as_accepted, mark_as_done]  # Добавляем действия


admin.site.register(Order, OrderAdmin)
