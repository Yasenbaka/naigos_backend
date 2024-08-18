from django.urls import path

from users.views.web_archive.avatar import get_user_avatar
from users.views.web_archive.change_new_archive import change_new_archive
from users.views.web_archive.current import get_current
from users.views.login import user_login, nopwd_login, nopwd_bot_check
from users.views.bot_archive.b_get_current import get_user_current

urlpatterns = [
    path('login', user_login),
    path('nopwd_login', nopwd_login),
    path('nopwd_code_check', nopwd_bot_check),

    path('archive/avatar', get_user_avatar),
    path('archive/current', get_current),
    path('archive/change_archive', change_new_archive),

    path('bot_archive/current', get_user_current),
]