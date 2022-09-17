import os
import pickle
import time
from html.parser import HTMLParser
from typing import List, Optional, Tuple

import requests
from cachecontrol import CacheControl
from cachecontrol.caches import FileCache
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from ..settings import MFA_CAS_URL, SETTING_PATH
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


def login_with_mfa(username: str, password: str, seed: str):
    """NUCTの多要素認証を突破し、認証済みCookieを持ったセッションオブジェクトを返す.

    Args:
        username (str): 認証のユーザー名（名大ID）
        password (str): 認証のパスワード（名大IDのパスワード）
        seed (str): 多要素認証のシード値

    Returns:
        requests.session: 認証済みCookieを持ったセッションオブジェクト
    """
    # sessionの開始
    session = requests.Session()
    retries = Retry(
        total=5,
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

    time.sleep(0.3)

    # username,passwordをpostする．多要素認証画面が返ってくる．
    auth_token_page = session.post(MFA_CAS_URL, data=payload)
    auth_token_page.raise_for_status()  # 200以外でエラー
    payload = get_payload(auth_token_page.text)
    payload.update({"token": get_totp_token(seed)})
    print("id & password auth: ", auth_token_page.status_code)

    time.sleep(0.3)

    # tokenを含めてpostする．nuctのトップ画面が返ってくる．
    nuct_top_page = session.post(MFA_CAS_URL, data=payload, timeout=(5.0, 5.0))
    nuct_top_page.raise_for_status()  # 200以外でエラー
    print("token auth: ", nuct_top_page.status_code)
    return session


def save_cookies(session: requests.Session) -> None:
    with open(SETTING_PATH + "/cookies.pkl", "wb") as f:
        pickle.dump(session.cookies, f)


def have_session():
    if not os.path.isfile(SETTING_PATH + "/cookies.pkl"):
        return False
    cookies = pickle.load(open(SETTING_PATH + "/cookies.pkl", "rb"))
    for cookie in cookies:
        if cookie.expires is None:
            continue
        if cookie.expires < int(time.time()):
            return False
    return True


def get_saved_session():
    session = requests.Session()
    cookies = pickle.load(open(SETTING_PATH + "/cookies.pkl", "rb"))
    session.cookies = cookies
    return session


def make_cached_session(session: requests.Session):
    cache_path = os.path.join(SETTING_PATH, ".cache")
    return CacheControl(session, cache=FileCache(cache_path))
