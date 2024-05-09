from django.conf import settings
from Constants.code_status import CodeStatus
import jwt

from bots.models import Bots

jwt_key = settings.SIMPLE_JWT['SIGNING_KEY']
jwt_alg = settings.SIMPLE_JWT['ALGORITHM']

token_details = CodeStatus().TokenCommunication().TokenDetailsStatus


def token_no_use() -> dict:
    return {
        'judge': False,
        'code': token_details.TOKEN_NO_USE[0],
        'message': token_details.TOKEN_NO_USE[1]
    }


def handle_token(token) -> dict:
    try:
        decode_token = jwt.decode(token, jwt_key, algorithms=[jwt_alg])
    except jwt.exceptions.ExpiredSignatureError:
        return {
            'judge': False,
            'code': token_details.TOKEN_EXPIRED_SIGNATURE_ERROR[0],
            'message': token_details.TOKEN_EXPIRED_SIGNATURE_ERROR[1]
        }
    except jwt.exceptions.DecodeError:
        return {
            'judge': False,
            'code': token_details.TOKEN_DECODE_ERROR[0],
            'message': token_details.TOKEN_DECODE_ERROR[1]
        }
    except jwt.exceptions.InvalidTokenError:
        return {
            'judge': False,
            'code': token_details.TOKEN_INVALID_ERROR[0],
            'message': token_details.TOKEN_INVALID_ERROR[1]
        }
    except jwt.PyJWTError:
        return {
            'judge': False,
            'code': token_details.TOKEN_UNKNOWN_ERROR[0],
            'message': token_details.TOKEN_UNKNOWN_ERROR[1]
        }
    else:
        # 请求令牌合法后的一些细节处理
        if decode_token['type'] == 'access_token':
            try:
                bot = Bots.objects.get(token=decode_token['access'])
            except Bots.DoesNotExist:
                return {
                    'judge': False,
                    'code': CodeStatus().BasicCommunication().UserArchive().USER_ARCHIVE_FOUNDED_FAILURE[0],
                    'message': CodeStatus().BasicCommunication().UserArchive().USER_ARCHIVE_FOUNDED_FAILURE[1]
                }
            if bot.safe_level == 0:
                return {
                    'judge': False,
                    'code': token_details.TOKEN_DESTROY[0],
                    'message': token_details.TOKEN_DESTROY[1]
                }
        return {
            'judge': True,
            'code': token_details.TOKEN_EFFECTIVE[0],
            'message': token_details.TOKEN_EFFECTIVE[1],
            'data': decode_token
        }
