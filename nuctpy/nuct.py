"""各種エンドポイントを叩くときに共通に必要な関数を提供する。"""
import json
from collections import namedtuple
from urllib.parse import urlparse

import requests

from . import settings
from .utilities import (
    get_saved_session,
    have_session,
    login_with_mfa,
    make_cached_session,
    save_cookies,
)

Var = namedtuple("Var", ("username", "password", "seed"))
Urls = namedtuple("Urls", ("portal", "direct", "domain"))


class NUCT:
    _vars = Var(
        username=settings.MEIDAI_ID, password=settings.MEIDAI_PWD, seed=settings.SEED
    )
    _urls = Urls(
        portal=settings.NUCT_ROOT + "/portal",
        direct=settings.NUCT_ROOT + "/direct",
        domain=urlparse(settings.NUCT_ROOT).netloc,
    )

    def __init__(self, use_old_cookie=True):
        """認証済みセッションオブジェクトと授業の一覧のjsonを持つ.
        Args:
            use_old_cookie: default=True. Cookieのキャッシュを無効にするオプション。

        Constants:
            site_data: 授業一覧のjson.
            site_id_title: { siteId: 授業名 }の形式の辞書のリスト。
        """
        self.session = self.create_session(use_old_cookie=use_old_cookie)
        _res = self.get(f"{self._urls.direct}/site.json?_limit=1000000")
        self.site_data = json.loads(_res.text)["site_collection"]
        self.site_id_title = {}
        for d in self.site_data:
            self.site_id_title.update({d["entityId"]: d["entityTitle"]})

    @classmethod
    def create_session(cls, use_old_cookie=True) -> requests.Session:
        """キャッシュがあれば用いてセッションをつくる.

        Returns:
            requests.Session: ログイン済みのセッション
        """
        if have_session() and use_old_cookie:
            session = get_saved_session()
        else:
            session = cls.get_new_session()
        save_cookies(session)
        return session

    @classmethod
    def get_new_session(cls, cached=True) -> requests.Session:
        """新しくログイン済みのセッションを作る.

        Args:
            cached (bool, optional): キャッシュを利用する. Defaults to True.

        Returns:
            requests.Session: ログイン済みのセッションオブジェクト
        """
        if cached:  # default
            session = login_with_mfa(
                cls._vars.username, cls._vars.password, cls._vars.seed
            )
            return make_cached_session(session)

        return login_with_mfa(cls._vars.username, cls._vars.password, cls._vars.seed)

    @staticmethod
    def formatter(func):
        """デコレーターとして用いる。

        機能
        1. フォーマットがjson/xmlであるか検証する。
        2. フォーマットがjsonの時は、メインデータを抜き出し、dictにして返す。
        """

        def wrapper(*args, **kwargs):
            # 関数を呼び出す時に明示的にformat=を指定しておかないと，
            # kwargsに値が入らない場合がある．
            fmt = kwargs["fmt"] if "fmt" in kwargs.keys() else "json"
            if fmt not in ["json", "xml"]:
                raise KeyError(
                    f"Invalid format: {fmt} is invalid. \
                        fmt must be json or xml. (Default is json)"
                )
            res = func(*args, **kwargs)
            res.raise_for_status()  # 200以外でエラー
            if res.status_code == 200:
                # jsonのときはdictに変換してあげて，メインの部分だけ抜き出してあげる
                if fmt == "json":
                    tmp = json.loads(res.text)
                    return tmp[tmp["entityPrefix"] + "_collection"]
                elif fmt == "xml":
                    return res
                else:
                    return res

        return wrapper

    def get(self, url, *args, **kwargs) -> requests.Response:
        """多要素認証にログイン済みの状態でURLにgetリクエストを送る. また、もしセッションが切れていたらセッションを作り直す。

        Args:
            url (url): https://*.nagoya-u.ac.jpのURLのみ許可されています。

        Returns:
            Request: レスポンス
        """
        parsed = urlparse(url)
        if parsed.netloc.split(".")[-3:] != self._urls.domain.split(".")[-3:]:
            raise ValueError(f"{urlparse(url).netloc}は許可されていません．")
        res = self.session.get(url, *args, **kwargs)
        if res.status_code == 401:
            self.session = self.get_new_session()
            self.get(url)
        res.raise_for_status()
        return res
