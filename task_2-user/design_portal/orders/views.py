from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView

from .forms import CreateOrderForm
from .models import Order, OrderPhoto


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'  # шаблон для отображения списка
    context_object_name = 'orders'

    def get_queryset(self):
        """
        Возвращает заказы текущего пользователя.
        """
        return Order.objects.filter(user=self.request.user)


class OrderCreateView(LoginRequiredMixin, CreateView):
    template_name = 'orders/create_order.html'
    form_class = CreateOrderForm
    success_url = reverse_lazy('order:list')

    def form_valid(self, form):
        order = form.save(commit=False)
        order.user = self.request.user
        order.save()

        photos = form.cleaned_data.get('photos')
        if photos:
            for photo in photos:
                OrderPhoto.objects.create(order=order, photo=photo)

        return super().form_valid(form)


class DeleteOrderView(LoginRequiredMixin, DeleteView):
    model = Order
    template_name = 'orders/confirm_delete.html'  # Укажите шаблон для подтверждения удаления
    success_url = reverse_lazy('order:list')  # URL для перенаправления после успешного удаления

    def get_queryset(self):
        """
        Ограничиваем доступ к удалению только для заказов текущего пользователя.
        """
        return super().get_queryset().filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        """
        Переопределяем метод post для проверки статуса перед удалением.
        """
        order = self.get_object()
        if order.status in ['Принято', 'Выполнено']:
            return HttpResponseForbidden("Удаление запрещено.")
        return super().post(request, *args, **kwargs)
