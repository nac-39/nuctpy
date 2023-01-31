import time
from html.parser import HTMLParser
from typing import List, Optional, Tuple

import requests

from ..settings import MFA_CAS_URL, NUCT_ROOT
from .totp import get_totp_token


class GetInputParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.params = {}

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        if tag == "input":
            tmp = {}
            for attr in attrs:
                if attr[0] == "name":
                    tmp["name"] = attr[1]
                elif attr[0] == "value":
                    tmp["value"] = attr[1]
            else:
                if "value" not in tmp.keys():
                    tmp["value"] = ""

            self.params.update({tmp["name"]: tmp["value"]})


def get_payload(html):
    parser = GetInputParser()
    parser.feed(html)
    payload = parser.params
    parser.close()
    return payload


def login_with_mfa(
    username: str, password: str, seed: str, print_log=True
) -> requests.Session:
    """NUCTの多要素認証を突破し、認証済みCookieを持ったセッションオブジェクトを返す.

    Args:
        username: 認証のユーザー名（名大ID）
        password: 認証のパスワード（名大IDのパスワード）
        seed: 多要素認証のシード値

    Returns:
        requests.Session: 認証済みCookieを持ったセッションオブジェクト
    """
    # sessionの開始
    session = requests.Session()
    session.headers[
        "User-Agent"
    ] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"  # noqa: #501

    def id_pwd_page_hook(r: requests.Response, *args, **kwargs):
        time.sleep(0)
        return r

    session.hooks["response"].append(id_pwd_page_hook)

    # Sakaiのログイン画面にアクセス
    auth_top_page = session.get(NUCT_ROOT + "portal/login")
    auth_top_page.raise_for_status()  # 200以外でエラー
    # formのname,valueの組を取得
    payload = get_payload(auth_top_page.text)
    payload.update({"username": username, "password": password})
    if print_log:
        print("top page: ", auth_top_page.status_code)

    # username,passwordをpostする．多要素認証画面が返ってくる．
    session.hooks["response"].append(id_pwd_page_hook)
    auth_token_page = session.post(MFA_CAS_URL, data=payload, allow_redirects=False)
    auth_token_page.raise_for_status()  # 200以外でエラー
    payload = get_payload(auth_token_page.text)
    if print_log:
        print("id & password auth: ", auth_token_page.status_code)

    def token_page_hooks(r: requests.Response, *args, **kwargs):
        if r.status_code == 401:
            payload = get_payload(r.text)
            payload.update({"token": get_totp_token(seed)})
            print("updated")
        elif r.status_code == 302:  # リダイレクトにsleepを挟む
            location = r.headers["Location"]
            if location == "/portal":
                r = session.get(NUCT_ROOT + location)
            else:
                r = session.get(location, cookies=r.cookies)
        return r

    session.hooks["response"].append(token_page_hooks)

    # tokenを含めてpostする．nuctのトップ画面が返ってくる．
    payload.update({"token": get_totp_token(seed)})
    count = 0
    while count <= 8:
        try:
            nuct_top_page = session.post(
                MFA_CAS_URL, data=payload, timeout=(5.0, 5.0), allow_redirects=False
            )
            nuct_top_page.raise_for_status()  # 200以外でエラー
            break
        except requests.exceptions.HTTPError as e:
            if print_log:
                print(e)
            time.sleep(3)
        count += 1
    if print_log:
        print("token auth: ", nuct_top_page.status_code)
    return session
