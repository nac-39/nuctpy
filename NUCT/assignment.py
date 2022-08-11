"""
Assignment

課題の一覧を操作するクラス．現在はAPIを叩くだけの関数のみ．
"""
from urllib.parse import unquote, urlparse

from .nuct import NUCT


class Assignment(NUCT):
    def __init__(self, session=None):
        super().__init__(session)
        self.assignment_url = self._urls.direct + "/assignment"

    @NUCT.formatter
    def site(self, siteid, format="json"):
        """
        ある授業のsiteidを指定して，その授業の課題一覧を取得する．
        
        Args:
            siteid: string  授業のid. 2022_1002140みたいな形式．
            format: stirng  jsonかxml．デフォルトはjson．
        
        Returns:
            res: list[dict]   NUCT.formatterによってフォーマットされた課題一覧のリストが返る．
        """
        url = self.assignment_url + f"/site/{siteid}.{format}"
        res = self.session.get(url)
        return res

    @NUCT.formatter
    def my(self, format="json"):
        """
        全ての課題一覧を取得する．
        
        Args:
            format: stirng  jsonかxml．デフォルトはjson．
        
        Returns:
            res: list[dict]   NUCT.formatterによってフォーマットされた課題一覧のリストが返る．
        """
        url = self.assignment_url + f"/my.{format}"
        res = self.session.get(url)
        return res
    
    @NUCT.formatter
    def item(self, assignmentId, format="json"):
        """
        試したけど使えなかった. 404が帰ってくる
        """
        url = self.assignment_url + f"/site/{assignmentId}.{format}"
        res = self.get_session().get(url)
        return res