import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status

from Constants.code_status import CodeStatus
from Handles.handle_login import handle_login


@require_http_methods(['POST'])
@csrf_exempt
def login_bot(request):
    appid, password = request.POST.get('appid'), request.POST.get('password')
    if appid is None or password is None:
        return JsonResponse({
            'code': CodeStatus().UNKNOWN_OR_MESSING_PARAMETER[0],
            'message': CodeStatus().UNKNOWN_OR_MESSING_PARAMETER[1]
        }, status=status.HTTP_403_FORBIDDEN)
    from naigos_backend.bot_pwd import get_pwd
    if password != get_pwd():
        return JsonResponse({
            'code': CodeStatus().BasicCommunication().UserArchive().USER_ARCHIVE_LOGIN_FAILURE[0],
            'message': f"{CodeStatus().BasicCommunication().UserArchive().USER_ARCHIVE_LOGIN_FAILURE[0]}！密码错误！"
        }, status=status.HTTP_403_FORBIDDEN)
    return handle_login(appid)
