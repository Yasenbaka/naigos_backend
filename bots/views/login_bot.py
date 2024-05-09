from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status

from Constants.code_status import CodeStatus
from Handles.handle_exchange_token_issue import handle_exchange_token_issue
from Handles.handle_login import handle_login
from Handles.handle_token import handle_token
from bots.models import Bots


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


@require_http_methods(['POST'])
@csrf_exempt
def exchange_token(request):
    token_details_status = CodeStatus().TokenCommunication().TokenDetailsStatus()
    user_archive_status = CodeStatus().BasicCommunication().UserArchive()
    (appid, access_token, refresh_token) = (request.POST.get('appid'),
                                            request.POST.get('access_token'),
                                            request.POST.get('refresh_token'))
    if appid is None or access_token is None or refresh_token is None:
        return JsonResponse({
            'code': token_details_status.TOKEN_MISSING_NECESSARY_VALUE[0],
            'error': token_details_status.TOKEN_MISSING_NECESSARY_VALUE[1]
        })
    try:
        bot = Bots.objects.get(appid=appid)
    except Bots.DoesNotExist:
        return JsonResponse({
            'code': user_archive_status.USER_ARCHIVE_FOUNDED_FAILURE[0],
            'error': user_archive_status.USER_ARCHIVE_FOUNDED_FAILURE[1]
        })
    if access_token != bot.access_token and refresh_token != bot.refresh_token:
        bot.safe_level -= 2
        bot.save()
        return JsonResponse({
            'code': token_details_status.TOKEN_INVALID_ERROR[0],
            'error': token_details_status.TOKEN_INVALID_ERROR[1]
        })
    decode_access_token = handle_token(access_token)
    if (not decode_access_token['judge'] and
            decode_access_token['code'] != token_details_status.TOKEN_EXPIRED_SIGNATURE_ERROR[0]):
        bot.safe_level -= 1
        bot.save()
        return JsonResponse({
            'code': decode_access_token['code'],
            'error': f"WEB请求令牌：{decode_access_token['message']}"
        })
    if ((not decode_access_token['judge']
            and decode_access_token['code'] == token_details_status.TOKEN_EXPIRED_SIGNATURE_ERROR[0])
            or decode_access_token['judge']):
        decode_refresh_token = handle_token(refresh_token)
        if not decode_refresh_token['judge']:
            return JsonResponse({
                'code': decode_refresh_token['code'],
                'error': f"WEB刷新令牌：{decode_refresh_token['message']}"
            })
        get_new_token = handle_exchange_token_issue(appid, decode_refresh_token['exp'])
        return JsonResponse({
            'code': CodeStatus().TokenCommunication().TokenIssuance().TOKEN_EXCHANGE_SUCCESS[0],
            'message': CodeStatus().TokenCommunication().TokenIssuance().TOKEN_EXCHANGE_SUCCESS[1],
            'data': {
                'access_token': get_new_token['access_token'],
                'refresh_token': get_new_token['refresh_token']
            }
        })






