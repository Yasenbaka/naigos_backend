import hashlib

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings

from Constants.code_status import CodeStatus
from Handles.handle_exchange_token_issue import handle_exchange_token_issue
from Handles.handle_bot_login import handle_login
from Handles.handle_bot_token import handle_token
from bots.models import Bots


SIGNING_KEY = settings.SIMPLE_JWT['SIGNING_KEY']


@require_http_methods(['POST'])
@csrf_exempt
def login_bot(request):
    appid, password = request.POST.get('appid'), request.POST.get('password')
    hash_password = (hashlib.sha256((SIGNING_KEY + password).encode())).hexdigest()
    try:
        bots = Bots.objects.get(bot_appid=appid)
    except Bots.DoesNotExist:
        return JsonResponse({
            'code': 1,
            'message': '该Bot信息不存在！'
        })
    db_save_password = bots.password
    if db_save_password != hash_password:
        return JsonResponse({
            'code': 1,
            'message': '登录密码不正确！'
        })
    return handle_login(appid)
