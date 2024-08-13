from django.conf import settings
import jwt

from users.models import Users

SIGNING_KEY = settings.SIMPLE_JWT['SIGNING_KEY']
ALGORITHM = settings.SIMPLE_JWT['ALGORITHM']


def handle_token(token: str) -> dict:
    try:
        decoded = jwt.decode(token, SIGNING_KEY, algorithms=[ALGORITHM])
    except jwt.exceptions.ExpiredSignatureError:
        return {
            'code': 1,
            'message': '令牌过期！'
        }
    except jwt.exceptions.DecodeError:
        return {
            'code': 1,
            'message': '令牌解码失败！'
        }
    except jwt.exceptions.InvalidTokenError:
        return {
            'code': 1,
            'message': '令牌非法！'
        }
    except jwt.PyJWTError:
        return {
            'code': 1,
            'message': '令牌严重错误！'
        }
    else:
        if decoded['source'] != 'web':
            return {
                'code': 1,
                'message': '非Web渠道的令牌来源！'
            }
        uuid = decoded['uuid']
        try:
            users = Users.objects.get(group_real_user_id=uuid)
        except Users.DoesNotExist:
            return {
                'code': 1,
                'message': '该用户UUID信息不存在！'
            }
        if users.safe_level == 0:
            return {
                'code': 1,
                'message': '用户安全等级高危，请重新登录！'
            }
        if users.safe_level < 0:
            return {
                'code': 1,
                'message': '用户档案已被冻结，网站端无法使用，请申诉解冻！'
            }
        return {
            'code': 0,
            'message': '令牌合法，安全！'
        }

