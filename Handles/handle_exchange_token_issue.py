from django.http import JsonResponse

from Handles.handle_bot_login import handle_login


def handle_exchange_token_issue(appid, exp) -> JsonResponse:
    return handle_login(appid, rule='exchange_token_issue', refresh_exp=exp)
