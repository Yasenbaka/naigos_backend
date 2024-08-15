from django.urls import path

from api.views.check_in import check_in
from api.views.signup import signup

from api.views.sogou_input_theme.get_theme_information import get_only_sogou_theme, get_all_sogou_themes

urlpatterns = [
    path('user/signup', signup, name='signup'),
    path('user/check_in', check_in),

    path('sogou_input_theme/get_only_item', get_only_sogou_theme),
    path('sogou_input_theme/get_all_item', get_all_sogou_themes),
]
