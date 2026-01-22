import webbrowser

from PyQt6.QtWidgets import QMainWindow

from PyQt6.QtGui import QKeySequence, QShortcut

from app.services.auth_store import AuthStore
from app.services.app_store import AppStore
from app.services.auth_service import AuthService

from app.client.widgets.blue_screen import BlueScreen

from app.client.controllers.session import Session

from app.client.views.login_view import LoginView
from app.client.views.signup_view import SignupView
from app.client.views.home_view import HomeView
from app.client.views.league_view import LeagueView
from app.client.views.team_view import TeamView

class FantasyApp(QMainWindow):
    '''
    Main app file for the application. Has functions for displaying all views.

    Also responsible for restoring user sessions on launch, otherwise 
    displaying the login view.
    '''
    def __init__(self):
        super().__init__()

        # instantiating blue screen, just in case ;)
        self.blue_screen = BlueScreen(self)

        close_shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        close_shortcut.activated.connect(self.close)

        self.setWindowTitle("SF6 Fantasy League")
        self.setFixedSize(1000, 800)

        if self._try_restore_session():
            self._try_restore_app_cache()
            self.show_home_view()
        else:
            self.show_login_view()

    def _try_restore_app_cache(self):
        cache = AppStore._load_all()

        # favourites
        favourites = cache.get("favourites")
        try:
            if isinstance(favourites[0], dict):
                Session.favourite_players = favourites[0]
        except Exception as e:
            pass

    def _try_restore_session(self) -> bool:
        data = AuthStore.load()
        if not data:
            return False

        try:
            base = AuthService.login_with_token(data)
            Session.auth_base = base
            Session.init_system_state()
            Session.init_services()
            Session.init_aesthetics()
            return True
        
        except Exception as e:
            # clears cached session if failed to login
            AuthStore.clear()
            AppStore.clear()
            return False
    
    def show_login_view(self):
        self.login_view = LoginView(app=self)
        self.setCentralWidget(self.login_view)

    def show_signup_view(self):
        self.signup_view = SignupView(app=self)
        self.setCentralWidget(self.signup_view)

    def show_home_view(self):
        self.home_view = HomeView(app=self)
        self.setCentralWidget(self.home_view)

    def show_league_view(self):
        self.league_view = LeagueView(app=self)
        self.setCentralWidget(self.league_view)

    def show_team_view(self):
        self.team_view = TeamView(app=self)
        self.setCentralWidget(self.team_view)

    def show_players_view(self):
        print("Players view requested")

    def show_leaderboards_view(self):
        print("Leaderboards view requested")

    def open_help(self):
        webbrowser.open(
            "https://github.com/bfararjeh/sf6-fantasy-league/blob/main/README.md#faqs"
        )

    def logout(self):
        Session.reset()
        AuthStore.clear()
        self.show_login_view()