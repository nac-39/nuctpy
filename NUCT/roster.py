from .nuct import NUCT


class Roster(NUCT):
    def __init__(self, session=None):
        super().__init__(session)
        self.roster_url = self._urls.direct + "/roster"

    @NUCT.formatter
    def site(self, siteid, format="json"):
        url = self.roster_url + f"/site/{siteid}.{format}"
        res = self.get_session().get(url)
        return res
