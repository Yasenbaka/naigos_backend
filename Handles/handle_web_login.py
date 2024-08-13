import time

import jwt
from django.http import JsonResponse

from naigos_backend import settings
from users.models import Users

ALGORITHM = settings.SIMPLE_JWT['ALGORITHM']
SIGNING_KEY = settings.SIMPLE_JWT['SIGNING_KEY']
ACCESS_TOKEN_LIFETIME = settings.TIME_JWT['ACCESS_TOKEN_LIFETIME']


def handle_login(uuid: str, rule: str = 'web', **kwargs) -> JsonResponse:
    token_header = {'alg': ALGORITHM, 'typ': 'JWT'}
    token_payload = {
        'uuid': uuid,
        'exp': int(time.time()) + ACCESS_TOKEN_LIFETIME,
        'source': rule
    }
    token = jwt.encode(headers=token_header, payload=token_payload, key=SIGNING_KEY, algorithm=ALGORITHM)
    users = Users.objects.get(group_real_user_id=uuid)
    if users.safe_level < 0:
        return JsonResponse({
            'code': 1,
            'message': '该用户奶果服务已冻结！'
        })
    users.safe_level = 10
    users.save()
    return JsonResponse({
        'code': 0,
        'message': '令牌签发！',
        'data': token
    })
