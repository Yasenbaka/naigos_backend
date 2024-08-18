import hashlib
import random
import time

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings

from Handles import handle_web_login
from Handles.handle_bot_token import handle_token
from users.models import Users, Password

SIGNING_KEY = settings.SIMPLE_JWT['SIGNING_KEY']


def handle_login_use(target):
    if '@' in target:
        try:
            users = Users.objects.get(email=target)
        except Users.DoesNotExist:
            return {
                'code': 1,
                'message': '未找到用户邮箱！'
            }
    elif len(target) == 11:
        try:
            users = Users.objects.get(phone=target)
        except Users.DoesNotExist:
            return {
                'code': 1,
                'message': '未找到用户手机号！'
            }
    else:
        try:
            users = Users.objects.get(id=target)
        except Users.DoesNotExist:
            return {
                'code': 1,
                'message': '未找到用户ID！'
            }
    return {
        'code': 0,
        'users': users,
    }


@require_http_methods(['POST'])
@csrf_exempt
def user_login(request) -> JsonResponse:
    login_type = request.POST.get('login_type')
    de_account = handle_login_use(request.POST.get('account'))
    if de_account['code'] != 0:
        return JsonResponse(de_account)
    users = de_account['users']
    uuid = users.group_real_user_id
    if login_type == 'normal':
        password = request.POST.get('password')
        try:
            password_model = Password.objects.get(uuid=uuid)
        except Password.DoesNotExist:
            return JsonResponse({
                'code': 1,
                'message': '该档案未设定密码，请使用无密码登录！'
            })
        encode_password = hashlib.sha256(str(password + SIGNING_KEY).encode()).hexdigest()
        db_password = password_model.password
        if encode_password != db_password:
            return JsonResponse({
                'code': 1,
                'message': '密码不正确！'
            })
        return handle_web_login.handle_login(users.group_real_user_id, rule='web')
    if login_type == 'nopwd':
        expiration_date = int(time.time()) + (3600 * 24 * 1)
        generate_code = ''.join(str(random.randint(0, 9)) for _ in range(6))
        try:
            password_model = Password.objects.get(uuid=uuid)
        except Password.DoesNotExist:
            Password.objects.create(uuid=uuid, code=generate_code, is_code=False, expiration_date=expiration_date)
        else:
            password_model.code, password_model.is_code, password_model.expiration_date = (
                generate_code, False, expiration_date
            )
            password_model.save()
        finally:
            return JsonResponse({
                'code': 0,
                'message': '验证码发送！有限期24小时！',
                'data': generate_code
            })
    return JsonResponse({
        'code': 1,
        'message': '未知的登录方式！'
    })


@require_http_methods(['POST'])
@csrf_exempt
def nopwd_login(request) -> JsonResponse:
    de_account = handle_login_use(request.POST.get('account'))
    if de_account['code'] != 0:
        return JsonResponse(de_account)
    users = de_account['users']
    uuid = users.group_real_user_id
    password_model = Password.objects.get(uuid=uuid)
    if password_model.code != request.POST.get('code'):
        return JsonResponse({
            'code': 1,
            'message': '验证码不正确！'
        })
    if not password_model.is_code:
        return JsonResponse({
            'code': 1,
            'message': '验证码未验证！'
        })
    if password_model.expiration_date < int(time.time()):
        return JsonResponse({
            'code': 1,
            'message': '验证码已过期！'
        })
    (password_model.is_code,
     password_model.code,
     password_model.expiration_date) = (False, None, None)
    password_model.save()
    return handle_web_login.handle_login(users.group_real_user_id, rule='web')


@require_http_methods(['POST'])
@csrf_exempt
def nopwd_bot_check(request):
    is_token = handle_token(request.headers['Authorization'])
    uuid = request.POST.get('real_user_id')
    bot_get_code = request.POST.get('code')
    if is_token['code'] == 1:
        return JsonResponse(is_token)
    try:
        password_model = Password.objects.get(uuid=uuid)
    except Password.DoesNotExist:
        return JsonResponse({
            'code': 1,
            'message': '没有找到档案对应验证码！'
        })
    if password_model.is_code:
        return JsonResponse({
            'code': 1,
            'message': '验证码被验证过，请在有效期内使用！'
        })
    if not password_model.code:
        return JsonResponse({
            'code': 1,
            'message': '没有验证码！'
        })
    if password_model.code == bot_get_code:
        password_model.is_code = True
        password_model.save()
        return JsonResponse({
            'code': 0,
            'message': '验证码成功验证！请在有效期内使用！'
        })
    password_model.code, password_model.is_code, password_model.expiration_date = None, False, None
    password_model.save()
    return JsonResponse({
        'code': 1,
        'message': '验证码各项不匹配，请重新获取验证码，多次不匹配可能会降低档案安全等级或冻结档案！'
    })

