import time

import jwt
from django.http import JsonResponse

from naigos_backend import settings

get_jwt_alg = settings.SIMPLE_JWT['ALGORITHM']
get_jwt_key = settings.SIMPLE_JWT['SIGNING_KEY']
get_access_token_lifetime = settings.TIME_JWT['ACCESS_TOKEN_LIFETIME']
get_refresh_token_lifetime = settings.TIME_JWT['REFRESH_TOKEN_LIFETIME']


def handle_login(bot_appid: str, bot_token: str):
    if bot_appid is None or bot_token is None:
        return JsonResponse({'code': 400, 'message': '缺少必要的键值！'})
    if bot_appid == "" and bot_token == "":
        token_header = {'typ': 'JWT', 'alg': get_jwt_alg}
        token_payload = {'bot_appid': bot_appid,
                         'exp': int(time.time()) + get_access_token_lifetime,
                         'rule': 'bot',
                         'type': 'access_token'}
        access_token = jwt.encode(headers=token_header, payload=token_payload, key=get_jwt_key, algorithm=get_jwt_alg)
        refresh_token = jwt.encode(headers=token_header, payload={
            'type': 'refresh_token',
            'access_token': access_token,
            'exp': int(time.time()) + get_refresh_token_lifetime,
            'rule': 'bot'
        }, key=get_jwt_key, algorithm=get_jwt_alg)
        return JsonResponse({
            'code': 200,
            'message': f"登入成功！自本次签发起，请求令牌有效期{get_access_token_lifetime/(3600*24)}天，"
                       f"刷新令牌有效期{get_refresh_token_lifetime/(3600*24)}天！",
            'data': {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        })
