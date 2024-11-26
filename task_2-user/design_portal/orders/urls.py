from django.urls import path
from . import views

app_name = "order"

urlpatterns = [
    path('list/', views.OrderListView.as_view(), name='list'),
    path('create/', views.OrderCreateView.as_view(), name='create'),
    path('delete/<int:pk>/', views.DeleteOrderView.as_view(), name='delete'),
    path('update-status/<int:pk>/', views.UpdateOrderStatusView.as_view(), name='update_status'),
]
