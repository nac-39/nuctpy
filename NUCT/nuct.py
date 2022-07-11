import json
from collections import namedtuple
from urllib.parse import urlparse
from .utirities import login_with_mfa
from . import settings

Var = namedtuple('Vars', ("username", "password", "seed"))
Urls = namedtuple('Urls', ("portal", "direct", "domain"))


class NUCT:
    def __init__(self):
        self._vars = Var(username=settings.MEIDAI_ID,
                         password=settings.MEIDAI_PWD,
                         seed=settings.SEED)
        self._urls = Urls(portal=settings.NUCT_ROOT+"/portal",
                          direct=settings.NUCT_ROOT+"/direct",
                          domain=urlparse(settings.NUCT_ROOT).netloc)
        self.session = login_with_mfa(self._vars.username,
                                      self._vars.password,
                                      self._vars.seed)
        _res = self.session.get(f"{self._urls.direct}/site.json?limit=0")
        self.site_data = json.loads(_res.text)


    @staticmethod
    def formatter(func):
        def wrapper(*args, **kwargs):
            # 関数を呼び出す時に明示的にformat=を指定しておかないと，
            # kwargsに値が入らない場合がある．
            format = kwargs["format"] if "format" in kwargs.keys() else "json"
            if not format in ["json", "xml"]:
                raise KeyError(
                f"Invalid format: {format} is invalid. format must be json or xml. (Default is json)")
            res = func(*args, **kwargs)
            # jsonのときはdictに変換してあげる
            if format == 'json':
                return json.loads(res)
            elif format == "xml":
                return res
            else:
                return res
        return wrapper
