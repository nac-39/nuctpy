import os
from urllib.parse import unquote, urlparse

from .nuct import NUCT


class Content(NUCT):
    def __init__(self, session=None):
        super().__init__(session)
        self.content_url = self._urls.direct + "/content"

    @NUCT.formatter
    def site(self, siteid, format="json"):
        """
        siteidの授業のリソースの詳細情報をとってくる

        Args:
            siteid: string  nuctのsiteid. 2022_1002140みたいな形式.
            format: string  json or xml

        Returns: 
            format=jsonのとき
            - dictに変換して返す.
            format=xmlのとき
            - xmlのまま返す.

        Errors:
            KeyError: formatがjsonかxmlでない時に送出する.
        """
        url = self.content_url + f"/site/{siteid}.{format}"
        res = self.session.get(url)
        return res

    def load_contents_url(self, siteid):
        """
        siteidの授業のリソースのURLのリストを返す.
        Content.site()のラッパー関数．

        Args: 
            siteid: string  nuctのsiteid. 2022_1002140みたいな形式.

        Returns:
            list    リソースのURLのリスト.
        """
        content_list = self.site(siteid)["content_collection"]
        url_list = []
        for d in content_list:
            if not d["url"].split("/")[-1] == "":
                url_list.append(d["url"])
        return url_list

    def load_contents(self, url_list: list[str], save_path=os.path.expanduser("~/Desktop")):
        """
        NUCTの認証が必要なURLからファイルをダウンロードするための関数.
        Content()の初期化が必要．
        一応, NUCT以外のドメインにはアクセスできないようにしておく.(セッション情報を送ってしまうと怖いため)

        Args:
            url_list: str   nuctのリソースのURLを想定.
            save_path: str  デフォルトはデスクトップ．ファイル名は含まない．

        Returns:
            無し．
        """
        for url in url_list:
            if urlparse(url).netloc != self._urls.domain:
                print(f"{urlparse(url).netloc}は許可されていません．")
                continue
            else:
                res = self.get_session().get(url, stream=True)
                # urlエンコーディングをデコードする
                filename = unquote(os.path.basename(url))
                # チャンクで分割して保存する
                with open(os.path.join(save_path, filename), "wb") as f:
                    for chunk in res.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            f.flush()
