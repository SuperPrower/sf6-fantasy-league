import json
import re
from sf6_fantasy_league.services.base_service import BaseService

class TeamService(BaseService):
    """
    Service for managing teams. Handles team setup tasks such as naming, draft
    priority submission, and draft order assignment.

    Methods:
    submit_team_name(team_name: str) -> bool
        Sets the team name for the authenticated manager after validating format.
        Returns True if successful.

    submit_player_list(player_list: list[str]) -> bool
        Submits a list of exactly 25 player names as the priority draft list for
        the manager. Ensures all players exist in the global player pool.
        Returns True if successful.
    """
    def submit_team_name(self, team_name: str):
        if len(team_name) < 4 or len(team_name) > 16:
            raise Exception("Team name must be inbetween 4 and 16 characters.")
        if not re.fullmatch(r'^\w+$', team_name):
            raise Exception("Team name must only include letters, numbers, and underscores.")

        self.verify_query(
            self.supabase
            .table("managers")
            .update({"team_name": team_name})
            .eq("user_id", self.user_id)
        )

        return True

    def submit_player_list(self, player_list: list[str]):
        if not self.get_my_team():
            raise Exception("You need to name your team first!")

        if len(player_list) != 25:
            raise Exception("Draft list must contain exactly 25 players.")

        player_pool = self.verify_query(
            self.supabase.table("players")
            .select("name")
            .in_("name", player_list)
            )

        if len(player_pool.data) != 25:
            raise Exception(f"The submitted player list is invalid.")

        self.verify_query(
            self.supabase.table("managers")
            .update({"player_priority_list": json.dumps(player_list)})
            .eq("user_id", self.user_id)
            )

        return True