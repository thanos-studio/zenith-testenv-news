from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import LoginForm, SignupForm


class LoginView(DjangoLoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, '환영합니다!')
        return super().form_valid(form)


class LogoutView(DjangoLogoutView):
    next_page = reverse_lazy('Main:press_list')


class SignupView(FormView):
    template_name = 'accounts/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('Main:press_list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, '회원가입이 완료되었습니다.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '입력 정보를 다시 확인해주세요.')
        return super().form_invalid(form)
