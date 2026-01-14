from app.services.team_service import TeamService
from app.services.league_service import LeagueService

class Session:
    VERSION = "1.0.0"

    user = None
    auth_base = None

    team_service = None
    league_service = None

    @classmethod
    def init_services(cls):
        if not cls.auth_base:
            raise RuntimeError("Cannot initialize services without auth_base.")

        cls.team_service = TeamService(cls.auth_base)
        cls.league_service = LeagueService(cls.auth_base)