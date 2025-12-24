import json
from uuid import uuid4
from sf6_fantasy_league.services.base_service import BaseService

class TeamService(BaseService):
    def submit_draft_priority(self, player_list: list[str]):
        if len(player_list) != 25:
            raise Exception("Draft list must contain exactly 25 players.")

        player_pool = self.verify_query(
            self.supabase.table("players")
            .select("name")
            .in_("name", player_list)
            )

        if not player_pool.data or len(player_pool.data) != 25:
            existing_names = [p["name"] for p in player_pool.data] if player_pool.data else []
            missing = set(player_list) - set(existing_names)
            raise Exception(f"The following players do not exist: {missing}")

        result = self.verify_query(
            self.supabase.table("managers")
            .update({"player_priority_list": json.dumps(player_list)})
            .eq("user_id", self.user_id)
            )

        return True