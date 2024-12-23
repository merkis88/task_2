from django.contrib.auth import logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, TemplateView

from .forms import LoginForm, RegisterUserForm
from .utils import send_verification_email, account_activation_token


# Главная страница
def index(request):
    return render(request, 'index.html')


# Регистрация
class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'registration/register.html'
    extra_context = {'title': "Register"}
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        self.request.session['user_email'] = user.email
        send_verification_email(self.request, user)
        return super().form_valid(form)


class UserConfirmEmailView(View):

    def get(self, request, uidb64, token):
        User = get_user_model()
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_object_or_404(User, pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('email_confirmed')
        else:
            return redirect('email_confirmation_failed')


class EmailConfirmedView(TemplateView):
    template_name = 'registration/email_confirmed.html'
    extra_context = {'title': 'Your email address has been activated'}


class EmailConfirmationFailedView(TemplateView):
    template_name = 'registration/email_confirmation_failed.html'
    extra_context = {'title': 'Invalid link'}


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
