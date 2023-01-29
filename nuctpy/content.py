import os
from urllib.parse import unquote, urlparse

from .nuct import NUCT

HOME_DIR = os.path.expanduser("~/Desktop")


class Content(NUCT):
    def __init__(self, use_old_cookie=True):
        super().__init__(use_old_cookie=use_old_cookie)
        self.content_url = self._urls.direct + "/content"

    @NUCT.formatter
    def site(self, siteid: str, fmt="json"):
        """Siteidの授業のリソースの詳細情報をとってくる.

        Args:
            siteid: nuctのsiteid. 2022_1002140みたいな形式.
            fmt:  "json"|"xml" 出力の形式

        Returns:
            res: NUCT.formatterによってフォーマットされた課題一覧のリストが返る．

        Errors:
            KeyError: formatがjsonかxmlでない時に送出する.
        """
        url = self.content_url + f"/site/{siteid}.{fmt}"
        res = self.get(url)
        return res

    def collect_url(self, siteid: str) -> list:
        """siteidの授業のリソースのURLのリストを返す. Content.site()のラッパー関数．

        Args:
            siteid: string  nuctのsiteid. 2022_1002140みたいな形式.

        Returns:
            url_list: リソースのurlのリスト
        """
        content_list = self.site(siteid)["content_collection"]
        url_list = []
        for d in content_list:
            if not d["url"].split("/")[-1] == "":
                url_list.append(d["url"])
        return url_list

    def load_contents(self, url: str, save_path=HOME_DIR):
        """NUCTの認証が必要なURLからファイルをダウンロードするための関数. Content()の初期化が必要． 一応,
        NUCT以外のドメインにはアクセスできないようにしておく.(セッション情報を送ってしまうと怖いため)

        Args:
            url_list: str   nuctのリソースのURLを想定.
            save_path: str  デフォルトはデスクトップ．ファイル名は含まない．

        Returns:
            無し．
        """
        if urlparse(url).netloc != self._urls.domain:
            print(f"{urlparse(url).netloc}は許可されていません．")
        else:
            res = self.get(url, stream=True)
            # urlエンコーディングをデコードする
            filename = unquote(os.path.basename(url))
            if filename == "":
                return
            # チャンクで分割して保存する
            with open(os.path.join(save_path, filename), "wb") as f:
                for chunk in res.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()
