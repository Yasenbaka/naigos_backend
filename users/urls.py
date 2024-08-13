from django.urls import path
from users.views.login import user_login, nopwd_login

urlpatterns = [
    path('login', user_login),
    path('nopwd_login', nopwd_login),
]