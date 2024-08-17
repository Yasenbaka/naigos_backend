from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from Handles import handle_web_token
from users.models import Users


@require_http_methods(['GET'])
@csrf_exempt
def get_current(request):
    de_token = handle_web_token.handle_token(request.headers.get('Authorization'))
    if de_token['code'] != 0:
        return JsonResponse(de_token)
    uuid = de_token['data']
    users = Users.objects.get(group_real_user_id=uuid)
    return JsonResponse({
        'code': 0,
        'message': '获取成功！',
        'data': {
            'nickname': users.nickname,
            'avatar': users.avatar,
            'id': users.id,
            'email': users.email,
            'score': users.score,
            'favorite': users.favorite,
            'city': users.city,
            'qq_id': users.qq_id,
            'uuid': users.group_real_user_id
        }
    })

