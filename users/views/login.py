import hashlib
import random
import time

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings

from Handles import handle_web_login
from users.models import Users, Password

SIGNING_KEY = settings.SIMPLE_JWT['SIGNING_KEY']


@require_http_methods(['POST'])
@csrf_exempt
def user_login(request) -> JsonResponse:
    account = request.POST.get('account')
    login_type = request.POST.get('login_type')
    if '@' in account:
        try:
            users = Users.objects.get(email=account)
        except Users.DoesNotExist:
            return JsonResponse({
                'code': 1,
                'message': '未找到用户邮箱！'
            })
    elif len(account) == 11:
        try:
            users = Users.objects.get(phone=account)
        except Users.DoesNotExist:
            return JsonResponse({
                'code': 1,
                'message': '未找到用户手机号！'
            })
    else:
        try:
            users = Users.objects.get(id=account)
        except Users.DoesNotExist:
            return JsonResponse({
                'code': 1,
                'message': '未找到用户ID！'
            })
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
    # qq_id, email, password, login_type = (request.POST.get('qq_id'),
    #                                       request.POST.get('email'),
    #                                       request.POST.get('password'),
    #                                       request.POST.get('type'))
    # if login_type == 'normal':
    #     if not qq_id and not email or not password:
    #         return JsonResponse({
    #             'code': 0,
    #             'message': '缺少必要的参数！'
    #         })
    #     elif qq_id and password:
    #         state: int = 1
    #     elif email and password:
    #         state: int = 2
    #     else:
    #         return JsonResponse({
    #             'code': 1,
    #             'message': '登录信息不正确！'
    #         })
    #     users = None
    #     if state == 1:
    #         try:
    #             users = Users.objects.get(qq_id=qq_id)
    #         except Users.DoesNotExist:
    #             return JsonResponse({
    #                 'code': 1,
    #                 'message': '未找到用户！'
    #             })
    #     if state == 2:
    #         try:
    #             users = Users.objects.get(email=email)
    #         except Users.DoesNotExist:
    #             return JsonResponse({
    #                 'code': 1,
    #                 'message': '未找到用户！'
    #             })
    #     try:
    #         password_mod = Password.objects.get(uuid=users.group_real_user_id)
    #     except Password.DoesNotExist:
    #         return JsonResponse({
    #             'code': 1,
    #             'message': '该档案未记录密码！'
    #         })
    #     db_password = password_mod.password
    #     encode_password = hashlib.sha256(str(password + SIGNING_KEY).encode()).hexdigest()
    #     if encode_password != db_password:
    #         return JsonResponse({
    #             'code': 1,
    #             'message': '密码错误！'
    #         })
    #     return handle_web_login.handle_login(users.group_real_user_id, rule='web')
    # if login_type == 'nopwd':
    #     qq_id, email = request.POST.get('qq_id'), request.POST.get('email')
    #     if not qq_id and not email:
    #         return JsonResponse({
    #             'code': 1,
    #             'message': '缺少必要参数！'
    #         })
    #     users = None
    #     if qq_id:
    #         try:
    #             users = Users.objects.get(qq_id=qq_id)
    #         except Users.DoesNotExist:
    #             return JsonResponse({
    #                 'code': 1,
    #                 'message': '未找到用户！'
    #             })
    #     if email:
    #         try:
    #             users = Users.objects.get(email=email)
    #         except Users.DoesNotExist:
    #             return JsonResponse({
    #                 'code': 1,
    #                 'message': '未找到用户！'
    #             })
    #     uuid = users.group_real_user_id
    #     expiration_date = int(time.time()) + (3600 * 24 * 1)
    #     generate_code = ''.join(str(random.randint(0, 9)) for _ in range(6))
    #     try:
    #         password_mod = Password.objects.get(uuid=uuid)
    #     except Password.DoesNotExist:
    #         Password.objects.create(uuid=uuid, code=generate_code, is_code=False, expiration_date=expiration_date)
    #     else:
    #         (password_mod.code,
    #          password_mod.is_code,
    #          password_mod.expiration_date) = (generate_code, False, expiration_date)
    #         password_mod.save()
    #     return JsonResponse({
    #         'code': 0,
    #         'message': '验证码发放，有效期24小时',
    #         'data': generate_code
    #     })
