from .nuct import NUCT


class Roster(NUCT):
    def __init__(self, session=None):
        super().__init__(session=session)
        self.roster_url = self._urls.direct + "/roster"

    @NUCT.formatter
    def site(self, siteid: str, fmt="json"):
        """サイトの登録者の一覧を取得します。
        Args:
            siteid: 講義のサイトID。例：2022_(7桁の数字)

        Returns:
            res: 登録者一覧の情報
        """
        url = self.roster_url + f"/site/{siteid}.{fmt}"
        res = self.get(url)
        return res
