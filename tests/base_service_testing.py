from random import choice
from copy import deepcopy
from .fixtures import TEST_USERS
from app.services.base_service import BaseService

def base_service_init(email, password):
    sv = BaseService(email, password)
    return sv

def test_a_user(sv):
    test_user = choice(TEST_USERS)
    test_email = test_user["email"]
    test_pass = test_user["password"]

    sv = base_service_init(test_email, test_pass)
    print(f"User ID: {sv.user_id}\nLeague ID: {sv.get_my_league()}")

def main():
    pass

if __name__ == "__main__":
    main()