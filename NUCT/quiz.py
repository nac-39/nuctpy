from .nuct import NUCT


class Quiz(NUCT):
    def __init__(self, session=None):
        super().__init__(session)
        self.quiz_url = self._urls.direct + "/sam_pub"

    @NUCT.formatter
    def context(self, siteid, format="json"):
        url = self.quiz_url + f"/context/{siteid}.{format}"
        res = self.session.get(url)
        return res
