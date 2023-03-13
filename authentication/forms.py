from django import forms
from django.contrib.auth.forms import AuthenticationForm


class AuthForm(AuthenticationForm):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control login-username',
                'placeholder': 'Username',
            }
        )
    )

    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control login-password',
                'placeholder': 'Password',
            }
        )
    )
