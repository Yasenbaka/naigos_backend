import random
import time

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from Handles.handle_token import handle_token
from users.models import Users, Judges


# Create your views here.

@require_http_methods(['POST'])
@csrf_exempt
def check_in(request):
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
    qq_id = users.qq_id
    try:
        Judges.objects.get(qq_id=qq_id)
    except Judges.DoesNotExist:
        Judges.objects.create(qq_id=qq_id)
    judges = Judges.objects.get(qq_id=qq_id)
    now_date = time.strftime("%Y%m%d")
    if judges.score == now_date:
        return JsonResponse({
            'code': 1,
            'message': '今日已经签到了！'
        })
    add_score = random.randint(15, 30)
    users.score += add_score
    new_score = users.score
    users.save()
    judges.score = now_date
    judges.save()
    return JsonResponse({
        'code': 0,
        'message': '签到成功',
        'data': {
            'add_score': add_score,
            'new_score': new_score,
        }
    })
