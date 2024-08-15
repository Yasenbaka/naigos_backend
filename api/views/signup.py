from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from Handles.handle_bot_token import handle_token
from users.models import Users


@require_http_methods(['POST'])
@csrf_exempt
def signup(request):
    is_token = handle_token(request.META.get('HTTP_AUTHORIZATION'))
    if is_token['code'] == 1:
        return JsonResponse(is_token)
    qq_id, real_user_id = request.POST.get('qq_id'), request.POST.get('real_user_id')
    if not qq_id or not real_user_id:
        return JsonResponse({
            'code': 1,
            'message': '缺少必要的参数！'
        })
    print(qq_id, real_user_id)
    try:
        Users.objects.get(qq_id=qq_id)
    except Users.DoesNotExist:
        try:
            Users.objects.get(group_real_user_id=real_user_id)
        except Users.DoesNotExist:
            Users.objects.create(group_real_user_id=real_user_id, qq_id=qq_id)
            return JsonResponse({
                'code': 0,
                'message': '记录成功！'
            })
        else:
            return JsonResponse({
                'code': 1,
                'message': '该UID号已经被记录在档案中！'
            })
    else:
        return JsonResponse({
            'code': 1,
            'message': '该QQ号已经被记录在档案中！'
        })
