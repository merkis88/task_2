from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import CustomUser


class RegisterUserForm(UserCreationForm):
    email = forms.CharField(label="E-mail",
                            widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label="Reply password",
                                widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'consent_data']
        widgets = {
            'consent_data': forms.CheckboxInput(attrs={'id': 'id_consent'})
        }


class LoginForm(AuthenticationForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['email', 'password']


class Registration(CreateView):
    model = CustomUser  # Укажите модель
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')  # URL для перенаправления после успешной регистрации
    fields = ['username', 'password', 'email']  # Поля формы
