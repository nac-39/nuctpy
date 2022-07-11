from .nuct import NUCT


class Content(NUCT):
    def __init__(self):
        super().__init__()
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
        if not format in ["json", "xml"]:
            raise KeyError(
                f"Invalid format: {format} is invalid. format must be json or xml. (Default is json)")
        url = self.content_url + f"/site/{siteid}.{format}"
        res = self.session.get(url)
        return res.text

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
