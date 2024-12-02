from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import CustomUser
from django.core.mail import send_mail  # Для отправки почты

class RegisterUserForm(UserCreationForm):
    email = forms.CharField(label="E-mail", widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'consent_data']
        widgets = {
            'consent_data': forms.CheckboxInput(attrs={'id': 'id_consent'})
        }

class LoginForm(AuthenticationForm):
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['email', 'password']

class Registration(CreateView):
    form_class = RegisterUserForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')  # Перенаправление после успешной регистрации

    def form_valid(self, form):
        """
        Сохраняем пользователя с деактивацией и отправляем письмо с подтверждением.
        """
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])  # Используем form.cleaned_data для пароля
        user.is_active = False  # Деактивация учетной записи
        user.is_activated = False  # Предположительно, у вас есть такое поле в модели CustomUser
        user.save()  # Сохраняем пользователя в базе данных

        # Отправка письма с подтверждением (здесь вы должны настроить ваше письмо)
        send_mail(
            'Подтверждение регистрации',  # Тема письма
            'Для активации вашей учетной записи, пожалуйста, подтвердите регистрацию.',  # Сообщение
            'from@example.com',  # Отправитель
            [user.email],  # Получатель
            fail_silently=False,
        )

        return super().form_valid(form)  # Перенаправляем на success_url
