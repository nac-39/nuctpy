"""Assignment.

課題の一覧を操作するクラス．現在はAPIを叩くだけの関数のみ．
"""

from .nuct import NUCT


class Assignment(NUCT):
    def __init__(self):
        super().__init__()
        self.assignment_url = self._urls.direct + "/assignment"

    @NUCT.formatter
    def site(self, siteid, fmt="json"):
        """ある授業のsiteidを指定して，その授業の課題一覧を取得する．

        Args:
            siteid:  授業のid. 2022_1002140みたいな形式．
            fmt: jsonかxml．デフォルトはjson．

        Returns:
            res: NUCT.formatterによってフォーマットされた課題一覧のリストが返る．
        """
        url = self.assignment_url + f"/site/{siteid}.{fmt}"
        res = self.get(url)
        return res

    @NUCT.formatter
    def my(self, fmt="json"):
        """全ての課題一覧を取得する．

        Args:
            fmt: jsonかxml．デフォルトはjson．

        Returns:
            res: NUCT.formatterによってフォーマットされた課題一覧のリストが返る．
        """
        url = self.assignment_url + f"/my.{fmt}"
        res = self.get(url)
        return res

    @NUCT.formatter
    def item(self, assignment_id, fmt="json"):
        """試したけど使えなかった.

        404が帰ってくる
        """
        url = self.assignment_url + f"/site/{assignment_id}.{fmt}"
        res = self.get_session().get(url)
        return res
