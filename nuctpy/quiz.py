from .nuct import NUCT


class Quiz(NUCT):
    def __init__(self):
        super().__init__()
        self.quiz_url = self._urls.direct + "/sam_pub"

    @NUCT.formatter
    def context(self, siteid: str, fmt="json"):
        """ある講義の小テスト一覧
        Args:
            siteid: 講義のサイトID。例：2022_(7桁数字)
        Returns:
            講義の小テストの情報
        """
        url = self.quiz_url + f"/context/{siteid}.{fmt}"
        res = self.get(url)
        return res
