from django.urls import path


from bots.views.login_bot import login_bot, exchange_token

urlpatterns = [
    path('login', login_bot),
    path('exchange_token', exchange_token),
]