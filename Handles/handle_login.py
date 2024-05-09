import time

import jwt
from django.http import JsonResponse

from Constants.code_status import CodeStatus
from naigos_backend import settings
from bots.models import Bots

get_jwt_alg = settings.SIMPLE_JWT['ALGORITHM']
get_jwt_key = settings.SIMPLE_JWT['SIGNING_KEY']
get_access_token_lifetime = settings.TIME_JWT['ACCESS_TOKEN_LIFETIME']
get_refresh_token_lifetime = settings.TIME_JWT['REFRESH_TOKEN_LIFETIME']


def handle_login(bot_appid: str, rule: str = 'login', **kwargs):
    refresh_token_exp, refresh_token_text = 0, None
    if rule == 'login':
        if bot_appid is None or len(bot_appid) == 0:
            return JsonResponse({
                'code': CodeStatus().UNKNOWN_OR_MESSING_PARAMETER[0],
                'error': CodeStatus().UNKNOWN_OR_MESSING_PARAMETER[1]
            })
        refresh_token_exp = int(time.time()) + get_refresh_token_lifetime
        refresh_token_text = f'刷新令牌有效期{get_refresh_token_lifetime / (3600 * 24)}天！'
    if rule == 'exchange_token_issue':
        refresh_token_exp = kwargs['refresh_exp']
        refresh_token_text = f'刷新令牌有效期是上次登入服务器起计时{get_refresh_token_lifetime / (3600 * 24)}天！'
    token_header = {'typ': 'JWT', 'alg': get_jwt_alg}
    token_payload = {'bot_appid': bot_appid,
                     'exp': int(time.time()) + get_access_token_lifetime,
                     'rule': 'bot',
                     'type': 'access_token'}
    access_token = jwt.encode(headers=token_header, payload=token_payload, key=get_jwt_key, algorithm=get_jwt_alg)
    refresh_token = jwt.encode(headers=token_header, payload={
        'type': 'refresh_token',
        'access_token': access_token,
        'exp': refresh_token_exp,
        'rule': 'bot'
    }, key=get_jwt_key, algorithm=get_jwt_alg)
    try:
        bot = Bots.objects.get(bot_appid=bot_appid)
    except Bots.DoesNotExist:
        return JsonResponse({
            'code': CodeStatus().BasicCommunication().UserArchive().USER_ARCHIVE_NOT_FOUND[0],
            'error': CodeStatus().BasicCommunication().UserArchive().USER_ARCHIVE_NOT_FOUND[1]
        })
    bot.access_token, bot.refresh_token, bot.safe_level = access_token, refresh_token, 10
    bot.save()
    return JsonResponse({
        'code': CodeStatus().BasicCommunication().UserArchive().USER_ARCHIVE_LOGIN_SUCCESS[0],
        'message': f"登入成功！自本次签发起，请求令牌有效期{get_access_token_lifetime / (3600 * 24)}天，"
                   f"{refresh_token_text}",
        'data': {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    })
