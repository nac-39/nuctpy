"""Announcement お知らせを取得するためのクラスです。"""
from typing import Literal

from .nuct import NUCT


class Announcement(NUCT):
    def __init__(self):
        super().__init__()
        self.announcement_url = self._urls.direct + "/announcement"

    @NUCT.formatter
    def site(self, siteid, fmt: Literal["json", "xml"] = "json"):
        """ある授業のお知らせを取得する関数です。
        Args:
            siteid: string 授業のサイトID
            fmt: "json"|"xml" 出力の形式

        Returns:
            dict: 一覧を辞書の配列で返す
        """
        url = self.announcement_url + f"/site/{siteid}.{fmt}"
        res = self.session.get(url)
        return res

    @NUCT.formatter
    def motd(self, fmt: Literal["json", "xml"] = "json"):
        """今日のお知らせの一覧を取得する関数です。
        Args:
            fmt: "json"|"xml" 出力の形式
        Returns:
            res: 一覧を辞書の配列で返す
        """
        url = self.announcement_url + f"/motd.{fmt}"
        res = self.session.get(url)
        return res

    @NUCT.formatter
    def user(self, fmt: Literal["json", "xml"] = "json"):
        """あるユーザーのお知らせの一覧を取得する関数です
         Args:
            fmt: "json"|"xml" 出力の形式
        Returns:
            res: 一覧を辞書の配列で返す

        """
        url = self.announcement_url + f"/user.{fmt}"
        res = self.session.get(url)
        return res
