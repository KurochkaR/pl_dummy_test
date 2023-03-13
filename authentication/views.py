from django.contrib.auth.views import LoginView

from authentication.forms import AuthForm


class MyLoginView(LoginView):
    form_class = AuthForm
