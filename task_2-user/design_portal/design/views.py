from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views import generic, View
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import LoginForm, RegisterUserForm


# Главная страница
def index(request):
    return render(request, 'index.html')


# Регистрация
class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'registration/register.html'
    extra_context = {'title': "Register"}
    success_url = reverse_lazy('login')


class LoginUser(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    extra_context = {'title': 'Авторизация'}


# Выход
def logout_view(request):
    logout(request)  # Выход пользователя
    return render(request, 'registration/logout.html')


class ProfileUser(LoginRequiredMixin, TemplateView):
    model = get_user_model()
    template_name = 'registration/profile.html'
    extra_context = {
        'title': "Профиль пользователя",
    }

    def get_success_url(self):
        return reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user
