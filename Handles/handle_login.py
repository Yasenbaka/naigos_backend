import time

import jwt
from django.http import JsonResponse

from bots.models import Bots
from naigos_backend import settings

ALGORITHM = settings.SIMPLE_JWT['ALGORITHM']
SIGNING_KEY = settings.SIMPLE_JWT['SIGNING_KEY']
ACCESS_TOKEN_LIFETIME = settings.TIME_JWT['ACCESS_TOKEN_LIFETIME']


def handle_login(bot_appid: str, rule: str = 'bot', **kwargs) -> JsonResponse:
    token_header = {'alg': ALGORITHM, 'typ': 'JWT'}
    token_payload = {
        'appid': bot_appid,
        'exp': int(time.time()) + ACCESS_TOKEN_LIFETIME,
        'rule': rule
    }
    token = jwt.encode(headers=token_header, payload=token_payload, key=SIGNING_KEY, algorithm=ALGORITHM)
    bots = Bots.objects.get(bot_appid=bot_appid)
    if bots.safe_level < 0:
        return JsonResponse({
            'code': 1,
            'message': '该BotAppid已被奶果服务冻结！'
        })
    bots.token = token
    bots.safe_level = 10
    bots.save()
    return JsonResponse({
        'code': 0,
        'message': '令牌签发！',
        'data': token
    })
