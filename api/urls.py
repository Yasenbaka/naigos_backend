from django.urls import path

from api.views.check_in import check_in
from api.views.signup import signup

urlpatterns = [
    path('user/signup', signup, name='signup'),
    path('user/check_in', check_in),
]
