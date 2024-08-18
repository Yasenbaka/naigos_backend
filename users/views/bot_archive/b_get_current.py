from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from Handles.handle_bot_token import handle_token
from users.models import Users


@require_http_methods(['POST'])
@csrf_exempt
def get_user_current(request):
    is_token = handle_token(request.headers['Authorization'])
    if is_token['code'] == 1:
        return JsonResponse(is_token)
    try:
        users = Users.objects.get(group_real_user_id=request.POST.get('real_user_id'))
    except Users.DoesNotExist:
        return JsonResponse({
            'code': 1,
            'message': '没有找到档案！'
        })
    return JsonResponse({
        'code': 0,
        'message': '获取成功！',
        'data': {
            'nickname': users.nickname,
            'id': users.id,
            'email': users.email,
            'score': users.score,
            'favorite': users.favorite,
            'qq_id': users.qq_id
        }
    })
