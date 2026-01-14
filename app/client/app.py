from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import Qt
from app.client.session import Session
from app.client.views.login_view import LoginView
from app.client.views.home_view import HomeView


class FantasyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Fantasy Street Fighter 6")
        self.resize(800, 600)

        self.show_login_view()
    
    def show_login_view(self):
        self.login_view = LoginView(app=self)
        self.setCentralWidget(self.login_view)

    def show_home_view(self):
        self.home_view = HomeView()

        # Connect navigation signals
        self.home_view.open_league_view.connect(self.show_league_view)
        self.home_view.open_team_view.connect(self.show_team_view)
        self.home_view.open_players.connect(self.show_players_view)
        self.home_view.open_leaderboards.connect(self.show_leaderboards_view)

        self.setCentralWidget(self.home_view)

    def show_league_view(self):
        print("League view requested")

    def show_team_view(self):
        print("Team view requested")

    def show_players_view(self):
        print("Players view requested")

    def show_leaderboards_view(self):
        print("Leaderboards view requested")