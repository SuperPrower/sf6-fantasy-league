from supabase import create_client
import re

SUPABASE_URL = "https://idnmrntzyljrppeocbpa.supabase.co"
SUPABASE_ANON_KEY = "sb_publishable_oLJyY3yFFqYoXP3-xvzTWA_aS6dGneP"

class UserService:
    def __init__(self):
        self.supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        self.current_user = None
        self.access_token = None

    def signup(self, email, password, manager_name):
        # Basic validation
        if len(password) < 8:
            raise Exception("Password must be at least 8 characters long.")
        if not re.fullmatch(r'^\w+$', manager_name):
            raise Exception("Username must only include letters, numbers, and underscores")

        # Sign up the user
        try:
            response = self.supabase.auth.sign_up({"email": email, "password": password})
            user = getattr(response, "user", None) or response.data
        except Exception as e:
            raise Exception(f"Signup failed: {e}")

        if not user:
            raise Exception(f"Signup failed: {response.data}")

        self.current_user = user

        # Insert manager row
        insert_data = {
            "user_id": user.id,  # keep as string; RLS uses user_id::uuid = auth.uid()
            "manager_name": manager_name,
        }

        result = self.supabase.table("managers").insert(insert_data).execute()

        # Check for errors
        if result.data is None:
            raise Exception(f"Failed to create manager row: {result.data}")

        return user.id

    def login(self, email, password):
        if not email or not password:
            raise ValueError("Email and password must be provided")

        try:
            response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            session = getattr(response, "session", None) or response.data
        except Exception as e:
            raise Exception(f"Login failed: {e}")

        if not session:
            raise Exception(f"Login failed: {response.data}")

        self.current_user = session.user
        self.access_token = getattr(session, "access_token", None)

        return {"user_id": self.current_user.id, "access_token": self.access_token}