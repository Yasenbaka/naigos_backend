from django.urls import path

from users.views.archive.avatar import get_user_avatar
from users.views.archive.current import get_current
from users.views.login import user_login, nopwd_login

urlpatterns = [
    path('login', user_login),
    path('nopwd_login', nopwd_login),

    path('archive/avatar', get_user_avatar),
    path('archive/current', get_current),
]