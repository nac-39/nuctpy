from dataclasses import dataclass
from typing import List

from .nuct import NUCT


class Roster(NUCT):
    def __init__(self, session=None):
        super().__init__(session)
        self.roster_url = self._urls.direct + "/roster"

    @dataclass
    class RosterSiteType:
        """Roster.site()の返り値
        Args:
            displayname: 講義の参加者の名前
            imageUrl: 講義の参加者のアイコン画像？
            entityReference: '/roster'
            entityUrl: 'https://ct.nagoya-u.ac.jp/direct/roster'
        """

        displayname: str
        image_url: str
        entity_reference: str
        entity_url: str

    @NUCT.formatter
    def site(self, siteid: str, fmt="json") -> List[RosterSiteType]:
        """サイトの登録者の一覧を取得します。
        Args:
            siteid: 講義のサイトID。例：2022_(7桁の数字)

        Returns:
            res: 登録者一覧の情報
        """
        url = self.roster_url + f"/site/{siteid}.{fmt}"
        res = self.session.get(url)
        return res
