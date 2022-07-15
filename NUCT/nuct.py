import json
from collections import namedtuple
from urllib.parse import urlparse
from .utilities import login_with_mfa
from . import settings

Var = namedtuple('Vars', ("username", "password", "seed"))
Urls = namedtuple('Urls', ("portal", "direct", "domain"))


class NUCT:
    _vars = Var(username=settings.MEIDAI_ID,
                password=settings.MEIDAI_PWD,
                seed=settings.SEED)
    _urls = Urls(portal=settings.NUCT_ROOT+"/portal",
                 direct=settings.NUCT_ROOT+"/direct",
                 domain=urlparse(settings.NUCT_ROOT).netloc)

    def __init__(self, session=None):
        if session is None:
            self.session = login_with_mfa(self._vars.username,
                                          self._vars.password,
                                          self._vars.seed
                                          )
        else:
            self.session = session
        _res = self.session.get(f"{self._urls.direct}/site.json?_limit=0")
        self.site_data = json.loads(_res.text)["site_collection"]

    @classmethod
    def create_session(cls):
        return login_with_mfa(cls._vars.username,
                              cls._vars.password,
                              cls._vars.seed)


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
            res.raise_for_status()  # 200以外でエラー
            if res.status_code == 200:
                # jsonのときはdictに変換してあげて，メインの部分だけ抜き出してあげる
                if format == 'json':
                    tmp = json.loads(res.text)
                    return tmp[tmp["entityPrefix"] + "_collection"]
                elif format == "xml":
                    return res
                else:
                    return res
        return wrapper
