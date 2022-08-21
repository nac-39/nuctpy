"""Announcement
お知らせを取得するためのクラスです。
"""
from .nuct import NUCT


class Announcement(NUCT):
    def __init__(self, session=None):
        super().__init__(session)
        self.announcement_url = self._urls.direct + "/announcement"

    @NUCT.formatter
    def site(self, siteid, format="json"):
        """ある授業のお知らせを取得する関数です。
        Args:
            siteid: string 授業のサイトID
            format: "json"|"xml" 出力の形式

        Returns:
            dict: 一覧を辞書の配列で返す
        """
        url = self.announcement_url + f"/site/{siteid}.{format}"
        res = self.session.get(url)
        return res

    @NUCT.formatter
    def motd(self, format="json"):
        """今日のお知らせの一覧を取得する関数です。
        Args:
            format: "json"|"xml" 出力の形式
        Returns:
            dict: 一覧を辞書の配列で返す
        """
        url = self.announcement_url + f"/motd.{format}"
        res = self.session.get(url)
        return res

    @NUCT.formatter
    def user(self, format="json"):
        """あるユーザーのお知らせの一覧を取得する関数です
         Args:
            format: "json"|"xml" 出力の形式
        Returns:
            dict: 一覧を辞書の配列で返す

        """
        url = self.announcement_url + f"/user.{format}"
        res = self.session.get(url)
        return res
