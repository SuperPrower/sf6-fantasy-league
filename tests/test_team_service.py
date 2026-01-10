import os
from random import shuffle, choice
from copy import deepcopy

from dotenv import load_dotenv
from .fixtures import ALICES_TEAM, TEST_USERS, PLAYER_POOL, TEAM_NAMES
from app.services.team_service import TeamService

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY")

def team_service_init(email, password):
    sv = TeamService(email, password)
    return sv

def submit_user_team(sv):
    teamname = choice(TEAM_NAMES)
    player_list = deepcopy(PLAYER_POOL)
    shuffle(player_list)
    player_list = player_list[:25]
    sv.create_team(teamname, player_list)
    print("Team submitted successfuly.")

def establish_all_test_user_teams():
    users = deepcopy(TEST_USERS)

    for user in users:
        sv = team_service_init(user["email"], user["password"])

        try:
            submit_user_team(sv)
            print(f"Team established for user: {user['email']}")
        except Exception as e:
            print(f"Error creating team for user {user['email']}: {e}")

def alice_teams():
    '''
    To be used after test_league_service.alice_league().

    Once the first 5 alphabetical users are all in a league and draft order
    is assigned, this function creates a team for each user.
    '''

    for i in range(5):
        user = TEST_USERS[i]
        sv = team_service_init(user["email"], user["password"])
        sv.create_team(TEAM_NAMES[i])

def alice_draft():
    '''
    Once Alice's league and team is established, this function drafts players
    to all users in the league. 

    ["Alice", "Dana", "Evan", "Bobert", "Charlie"]
    ^ pick direction for reference
    '''
    sv_list = []
    a_team = ALICES_TEAM
    a_team.reverse()

    for i in range(5):
        user = a_team[i]
        sv_list.append(team_service_init(user["email"], user["password"]))
    
    for i in range(5):
        try:
            print(f"Picking player for user {a_team[i]["manager_name"]}")
            sv_list[i].pick_player(choice(PLAYER_POOL))
        except Exception as e:
            print(f"Failed to pick player for user {a_team[i]["manager_name"]}: {e}")
            continue

def main():
    pass

if __name__ == "__main__":
    main()