from urllib.parse import unquote, urlparse
from .nuct import NUCT


class Assignment(NUCT):
    def __init__(self, session=None):
        super().__init__(session)
        self.assignment_url = self._urls.direct + "/assignment"

    @NUCT.formatter
    def site(self, siteid, format="json"):
        url = self.assignment_url + f"/site/{siteid}.{format}"
        res = self.session.get(url)
        return res
    
    @NUCT.formatter
    def my(self, format="json"):
        url = self.assignment_url + f"/my.{format}"
        res = self.session.get(url)
        return res
    
    @NUCT.formatter
    def item(self, assignmentId, format="json"):
        """
        試したけど使えなかった. 404が帰ってくる
        """
        url = self.assignment_url + f"/site/{assignmentId}.{format}"
        res = self.session.get(url)
        return res