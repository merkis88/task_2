from django import template

from orders.models import Order

register = template.Library()


@register.inclusion_tag('orders/list_tags.html', takes_context=True)
def show_all_tags(context):
    user = context['request'].user
    orders = Order.objects.filter(status=Order.ChoicesStatus.DONE.value, user=user)[:4]

    # Подсчитываем количество заявок со статусом "Принято" для текущего пользователя
    accepted_count = Order.objects.filter(status=Order.ChoicesStatus.ACCEPT.value, user=user).count()

    return {
        'orders': orders,
        'accepted_count': accepted_count,
    }
