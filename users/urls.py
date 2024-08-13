from django.urls import path
from users.views.login import user_login

urlpatterns = [
    path('login', user_login),
]