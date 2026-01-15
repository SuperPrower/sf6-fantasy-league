from supabase import create_client
from app.db.supabase_client import get_supabase_client
from app.services.base_service import BaseService

class AuthService:
    @staticmethod
    def login(email: str, password: str) -> BaseService:
        '''
        Logs in with an email and password and returns a base service object.
        '''
        if not email or not password:
            raise ValueError("Email and password must be provided.")

        supabase = get_supabase_client()

        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        session = response.session

        return BaseService(
            supabase=supabase,
            user_id=response.user.id,
            access_token=session.access_token,
            refresh_token=session.refresh_token
        )

    @staticmethod
    def login_with_token(token_data: dict) -> BaseService:
        '''
        Logs in with a saves session (stored in 
        AppData.Roaming.SF6FantasyLeague) and returns a base service object.
        '''
        refresh_token = token_data.get("refresh_token")
        if not refresh_token:
            raise ValueError("Missing refresh token for session restoration")

        supabase = get_supabase_client()

        try:
            auth_response = supabase.auth.refresh_session(refresh_token)
            session = auth_response.session  # <-- the real session object

            return BaseService(
                supabase=supabase,
                user_id=session.user.id,
                access_token=session.access_token,
                refresh_token=session.refresh_token
            )

        except Exception as e:
            raise Exception(f"Failed to restore session: {e}")