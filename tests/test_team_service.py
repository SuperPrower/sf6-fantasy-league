import os
from random import shuffle, choice
from copy import deepcopy

from dotenv import load_dotenv
import supabase
from .fixtures import TEST_USERS, PLAYER_POOL, TEAM_NAMES
from sf6_fantasy_league.services.team_service import TeamService

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY")

def team_service_init(email, password):
    sv = TeamService(email, password)
    return sv

def submit_user_team_name(sv):
    teamname = choice(TEAM_NAMES)
    sv.submit_team_name(teamname)
    print("Team name submitted successfuly.")

def submit_user_player_list(sv):
    player_list = deepcopy(PLAYER_POOL)
    shuffle(player_list)
    player_list = player_list[:25]

    sv.submit_player_list(player_list)
    print("Player list submitted successfuly.")

def establish_all_test_user_teams():
    users = deepcopy(TEST_USERS)

    for user in users:
        sv = team_service_init(user["email"], user["password"])
        submit_user_team_name(sv)
        submit_user_player_list(sv)
        print(f"Team established for user: {user['email']}")

def main():
    establish_all_test_user_teams()

if __name__ == "__main__":
    main()