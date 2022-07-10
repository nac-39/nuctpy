import requests
from urllib.parse import urljoin, urlencode
import json
from .utirities import return_cookie, in_expiry_date
from . import settings


class NUCT:
    NUCT_DOMAIN = settings.NUCT_DOMAIN

    def __init__(self):
        self._option = {
            # TODO: NamedTuple使った方が綺麗かも
            "MFA_CAS_URL": settings.MFA_CAS_URL,
            "NUCT_URL": urljoin(settings.NUCT_DOMAIN, "/portal"),
            "MEIDAI_ID": settings.MEIDAI_ID,
            "MEIDAI_PWD": settings.MEIDAI_PWD,
            "SEED": settings.SEED,
        }
        self.cookie = return_cookie(self._option)
        self._site = None
        self._my_assignment = None
        self.content_data = {}

    def _latest_cookie(self):
        if not in_expiry_date(self.cookie):
            self.cookie = return_cookie(self._option)
        return self.cookie

    def _fetch_with_mfa_cookie(self, url):
        session = requests.Session()
        for cookie in self._latest_cookie():
            session.cookies.set(cookie["name"], cookie["value"])
        res = session.get(url, timeout=10)
        return res.content.decode('utf8', 'ignore')

    def fetch_site(self, limit=0, format="json"):
        if self.site == None:
            url = urljoin(self.NUCT_DOMAIN,
                          f"direct/site.{format}?limit={limit}")
            res = self._fetch_with_mfa_cookie(url)
            if format == "json":
                self._site = json.loads(res)
            else:
                # TODO: xml形式にも対応する．
                self._site = res
        return self._site

    def assignment(self, format="json"):
        if self._my_assignment == None:
            url = urljoin(self.NUCT_DOMAIN,
                          f"direct/assignment/my.{format}")
            res = self._fetch_with_mfa_cookie(url)
            if format == "json":
                self._my_assignment = json.loads(res)
            else:
                # TODO: xml形式にも対応する．
                self._my_assignment = res
        return self._my_assignment

    def assignment_by_siteid(self, siteid, format="json"):
        url = urljoin(self.NUCT_DOMAIN,
                      f"direct/assignment/site/{siteid}.{format}")
        res = self._fetch_with_mfa_cookie(url)
        if format == "json":
            return json.loads(res)
        else:
            # TODO: xml形式にも対応する．
            return res
    
    def assignment_by_assignmentid(self, assignmentid, format="json"):
        url = urljoin(self.NUCT_DOMAIN,
                      f"direct/assignment/item/{assignmentid}.{format}")
        res = self._fetch_with_mfa_cookie(url)
        if format == "json":
            return json.loads(res)
        else:
            # TODO: xml形式にも対応する．
            return res
        
    def content(self, siteid):
        url = urljoin(self.NUCT_DOMAIN,
                      f"direct/content/site/{siteid}.json")
        res = self._fetch_with_mfa_cookie(url)
        self.content_data[siteid] = json.loads(res)["content_collection"]
        return self.content_data[siteid]
    
    def load_content_with_cookie(self, url):
        # TODO:cookieを用いてリソースをダウンロードする
        pass
