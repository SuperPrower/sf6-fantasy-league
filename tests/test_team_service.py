from random import choice
from dotenv import load_dotenv
from supabase import create_client
from sf6_fantasy_league.services.team_service import TeamService
from sf6_fantasy_league.services.user_service import UserService
from tests.fixtures.player_lists import PLAYER_LISTS
from tests.fixtures.users import TEST_USERS
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY")

def test_priority_submit(team_service):
    draft_list = choice(PLAYER_LISTS)

    try:
        team_service.submit_draft_priority(player_list=draft_list)
        print(f"Draft priority submitted successfully.")
    except Exception as e:
        print(f"Draft submission failed: {e}")

def delete_test_priority(user_id):
    client = create_client(SUPABASE_URL, SUPABASE_SECRET_KEY)
    
    try:
        result = (
            client
            .table("managers")
            .update({"player_priority_list": None})
            .eq("user_id", user_id)
            .execute()
        )

        print(f"Player priority list deleted successfully.")

    except Exception as e:
        print(f"Error deleting team: {e}")

def main():
    users = TEST_USERS.copy()
    user = choice(users)
    user_service = UserService()
    login = user_service.login(user["email"], user["password"])
    print(f"Login successful for {user['email']}")

    team_service = TeamService(access_token=login["access_token"], user_id=login["user_id"])

    test_priority_submit(team_service)
    input("Press Enter to begin draft list deletion.")
    delete_test_priority(login["user_id"])

if __name__ == "__main__":
    main()