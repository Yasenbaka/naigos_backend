from Handles.handle_login import handle_login


def handle_exchange_token_issue(appid, exp) -> dict:
    return handle_login(appid, rule='exchange_token_issue', refresh_exp=exp)
