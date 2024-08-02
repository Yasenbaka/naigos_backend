from django.urls import path


from bots.views.login_bot import login_bot

urlpatterns = [
    path('login', login_bot),
]
