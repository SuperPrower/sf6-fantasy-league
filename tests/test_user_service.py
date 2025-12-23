import re
from sf6_fantasy_league.db.user_service import UserService

def main():
    user_service = UserService()
    email = "testUser@gmail.com"
    password = "HGUIgySDFGSDT7896GHKG"
    manager_name = "TestUser"

    try:
        user_id = user_service.signup(email, password, manager_name)
        print(f"Signup successful! User ID: {user_id}")
    except Exception as e:
        print(f"{e}")

    try:
        session = user_service.login(email, password)
        print(f"Login successful!")
    except Exception as e:
        print(f"{e}")

if __name__ == "__main__":
    main()