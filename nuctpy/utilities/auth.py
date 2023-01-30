from html.parser import HTMLParser
from typing import List, Optional, Tuple

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from ..settings import MFA_CAS_URL
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


def login_with_mfa(username: str, password: str, seed: str) -> requests.Session:
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
    retries = Retry(
        total=2,
        backoff_factor=1,
        allowed_methods=["POST"],
        status_forcelist=[401, 500, 502, 503, 504],
    )
    session.mount("https://", HTTPAdapter(max_retries=retries))
    session.mount("http://", HTTPAdapter(max_retries=retries))

    # 認証のトップページにアクセス
    auth_top_page = session.get(MFA_CAS_URL)
    auth_top_page.raise_for_status()  # 200以外でエラー
    # formのname,valueの組を取得
    payload = get_payload(auth_top_page.text)
    payload.update({"username": username, "password": password})
    print("top page: ", auth_top_page.status_code)

    # username,passwordをpostする．多要素認証画面が返ってくる．
    auth_token_page = session.post(MFA_CAS_URL, data=payload)
    auth_token_page.raise_for_status()  # 200以外でエラー
    payload = get_payload(auth_token_page.text)
    print("id & password auth: ", auth_token_page.status_code)

    def upload_payload(r: requests.Response, *args, **kwargs):
        if r.status_code == 401:
            payload = get_payload(r.text)
            payload.update({"token": get_totp_token(seed)})
        return r

    session.hooks["response"].append(upload_payload)

    # tokenを含めてpostする．nuctのトップ画面が返ってくる．
    payload.update({"token": get_totp_token(seed)})
    nuct_top_page = session.post(MFA_CAS_URL, data=payload, timeout=(5.0, 5.0))
    nuct_top_page.raise_for_status()  # 200以外でエラー
    print("token auth: ", nuct_top_page.status_code)
    return session
