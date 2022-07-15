import requests
from html.parser import HTMLParser
import time
from .totp import get_totp_token

url = "https://auth-mfa.nagoya-u.ac.jp/cas/login?service=https%3A%2F%2Fct.nagoya-u.ac.jp%2Fsakai-login-tool%2Fcontainer"


class GetInputParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.params = {}

    def handle_starttag(self, tag: str, attrs: list[tuple]) -> None:
        if tag == "input":
            tmp = {}
            for attr in attrs:
                if attr[0] == "name":
                    tmp["name"] = attr[1]
                elif attr[0] == "value":
                    tmp["value"] = attr[1]
            else:
                if not "value" in tmp.keys():
                    tmp["value"] = ""

            self.params.update({tmp["name"]: tmp["value"]})


def get_payload(html):
    parser = GetInputParser()
    parser.feed(html)
    payload = parser.params
    parser.close()
    return payload


def login_with_mfa(USER_NAME: str, PASSWORD: str, SEED: str) -> requests.session:
    # sessionの開始
    session = requests.Session()

    # 認証のトップページにアクセス
    auth_top_page = session.get(url)
    auth_top_page.raise_for_status()  # 200以外でエラー
    # formのname,valueの組を取得
    payload = get_payload(auth_top_page.text)
    payload.update({"username": USER_NAME, "password": PASSWORD})
    print("top page: ", auth_top_page.status_code)

    time.sleep(0.3)

    # username,passwordをpostする．多要素認証画面が返ってくる．
    auth_token_page = session.post(url, data=payload)
    auth_token_page.raise_for_status()  # 200以外でエラー
    payload = get_payload(auth_token_page.text)
    payload.update({"token": get_totp_token(SEED)})
    print("id & password auth: ", auth_token_page.status_code)

    time.sleep(0.3)

    # tokenを含めてpostする．nuctのトップ画面が返ってくる．
    nuct_top_page = session.post(url, data=payload)
    nuct_top_page.raise_for_status()  # 200以外でエラー
    print("token auth: ", nuct_top_page.status_code)
    return session
    

