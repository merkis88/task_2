from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),  # Главная страница
    path('register/', views.RegisterUser.as_view(), name='register'),  # Регистрация
    path('login/', views.LoginUser.as_view(), name='login'),  # Вход
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileUser.as_view(), name='profile'),  # Каталог
    path('confirm-email/<str:uidb64>/<str:token>/', views.UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email-confirmed/', views.EmailConfirmedView.as_view(), name='email_confirmed'),
    path('confirm-email-failed/', views.EmailConfirmationFailedView.as_view(), name='email_confirmation_failed'),
]
