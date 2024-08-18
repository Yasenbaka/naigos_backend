from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from Handles import handle_web_token
from users.models import Users, Judges

from naigos_backend.mysql_details import get_mysql_details
import pymysql


@require_http_methods(['GET'])
@csrf_exempt
def change_new_archive(request):
    de_token = handle_web_token.handle_token(request.headers.get('Authorization'))
    if de_token['code'] != 0:
        return JsonResponse(de_token)
    uuid = de_token['data']
    users = Users.objects.get(group_real_user_id=uuid)
    qq_id = users.qq_id
    judge = Judges.objects.get(qq_id=qq_id)
    if judge.transfer_archive:
        return JsonResponse({
            'code': 1,
            'message': '档案曾经迁移过！'
        })
    conn = pymysql.connect(host=get_mysql_details()['url'],
                           user=get_mysql_details()['username'],
                           password=get_mysql_details()['password'],
                           database=get_mysql_details()['database'])
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT username, city, score, favorite FROM archives WHERE qq_id = {qq_id};")
        result = cursor.fetchone()
    except pymysql.MySQLError as e:
        print(f"数据库错误: {e}")
        return JsonResponse({
            'code': 1,
            'message': '数据库出错！'
        })
    finally:
        conn.close()
    if result:
        print(result)
        users.nickname, users.city = result[0], result[1]
        today = datetime.now()
        days: int = int((today - (datetime((today.year - 1), 12, 21))).days) * 10
        users.score += (result[2] + days)
        users.favorite += result[3]
        users.save()
        judge.transfer_archive = True
        judge.save()
        return JsonResponse({
            'code': 0,
            'message': '成功转移到新奶果档案！'
        })
    else:
        judge.transfer_archive = True
        judge.save()
        return JsonResponse({
            'code': 1,
            'message': '未找到该QQ号的旧奶果档案信息！'
        })
