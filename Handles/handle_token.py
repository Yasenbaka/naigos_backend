from django.conf import settings
from Constants.code_status import CodeStatus
import jwt

from bots.models import Bots

SIGNING_KEY = settings.SIMPLE_JWT['SIGNING_KEY']
ALGORITHM = settings.SIMPLE_JWT['ALGORITHM']


def handle_token(token: str) -> dict:
    try:
        decode_token = jwt.decode(token, SIGNING_KEY, algorithms=[ALGORITHM])
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
        # 请求令牌合法后的一些细节处理
        appid = decode_token['appid']
        try:
            bots = Bots.objects.get(bot_appid=appid)
        except Bots.DoesNotExist:
            return {
                'code': 1,
                'message': '该Bot信息不存在！'
            }
        if bots.safe_level == 0:
            return {
                'code': 1,
                'message': '该Bot令牌安全等级：低，需要管理员重新登录！'
            }
        if bots.safe_level < 0:
            return {
                'code': 1,
                'message': '该BotAppid已被奶果服务冻结！'
            }
        db_token = bots.token
        if token != db_token:
            bots.safe_level = 0
            return {
                'code': 1,
                'message': '令牌合法，但已经危险！'
            }
        return {
            'code': 0,
            'message': '令牌合法，安全！'
        }
