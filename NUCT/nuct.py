import requests
from urllib.parse import urljoin, urlencode
import json
from collections import namedtuple
from .utirities import login_with_mfa
from . import settings

Var = namedtuple('Vars', ("username", "password", "seed"))
Urls = namedtuple('Urls', ("portal", "direct", "domain"))


class NUCT:
    def __init__(self):
        self._vars = Var(username=settings.MEIDAI_ID,
                         password=settings.MEIDAI_PWD,
                         seed=settings.SEED)
        self._urls = Urls(portal=settings.NUCT_DOMAIN+"/portal",
                          direct=settings.NUCT_DOMAIN+"/direct",
                          domain=settings.NUCT_DOMAIN)
        self.session = login_with_mfa(self._vars.username,
                                      self._vars.password,
                                      self._vars.seed)

    def fetch(self, url):
        res = self.session.get(url)

    @staticmethod
    def formatter(func):
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            # 関数を呼び出す時に明示的にformat=を指定しておかないと，
            # kwargsに値が入らない場合がある．
            format = kwargs["format"] if "format" in kwargs.keys() else "json"
            # jsonのときはdictに変換してあげる
            if format == 'json':
                return json.loads(res)
            elif format == "xml":
                return res
            else:
                return res
        return wrapper
