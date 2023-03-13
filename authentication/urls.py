from django.urls import path
from django.contrib.auth.views import LogoutView
from authentication.views import MyLoginView


urlpatterns = [
    path('mylogin/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    ]