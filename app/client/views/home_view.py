import webbrowser
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
)
from PyQt6.QtCore import Qt, pyqtSignal

from app.client.session import Session


class HomeView(QWidget):
    open_league_view = pyqtSignal()
    open_team_view = pyqtSignal()
    open_players = pyqtSignal()
    open_leaderboards = pyqtSignal()
    open_help = pyqtSignal()
    logout = pyqtSignal()

    def __init__(self, app):
        super().__init__()
        self.app = app
        self._build_ui()

    def _build_ui(self):
        # --- Main vertical layout ---
        root_layout = QVBoxLayout()
        root_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root_layout.setSpacing(20)

        # ----- Central content (title, user info, main buttons) -----
        # This is your existing content
        title = QLabel("Home")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold;")

        username = Session.user or "Player"
        user_label = QLabel(f"Welcome, {username}")
        user_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        user_label.setStyleSheet("font-size: 16px; color: #555555;")

        # Main navigation buttons (league/team/players/leaderboards)
        league_button = QPushButton("Go to League")
        team_button = QPushButton("Go to Team")
        player_button = QPushButton("View Players")
        leaderboard_button = QPushButton("View Leaderboards")
        for button in (league_button, team_button, player_button, leaderboard_button):
            button.setFixedHeight(42)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setStyleSheet("""
                QPushButton {
                    font-size: 14px; font-weight: bold;
                    background-color: #2d7df6; color: white;
                    border-radius: 6px;
                }
                QPushButton:hover { background-color: #1f6ae1; }
                QPushButton:pressed { background-color: #1a5bc4; }
            """)

        league_button.clicked.connect(self.open_league_view.emit)
        team_button.clicked.connect(self.open_team_view.emit)
        player_button.clicked.connect(self.open_players.emit)
        leaderboard_button.clicked.connect(self.open_leaderboards.emit)

        # Add central content to root layout
        root_layout.addWidget(title)
        root_layout.addWidget(user_label)
        root_layout.addSpacing(10)
        root_layout.addSpacing(20)
        root_layout.addWidget(league_button)
        root_layout.addWidget(team_button)
        root_layout.addWidget(player_button)
        root_layout.addWidget(leaderboard_button)

        # ----- Top-right floating buttons -----
        self.top_right_widget = QWidget(self)
        top_layout = QHBoxLayout(self.top_right_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.addStretch()  # push buttons to the right

        help_button = QPushButton("Help")
        help_button.setFixedSize(60, 25)
        help_button.clicked.connect(self.open_help.emit)
        logout_button = QPushButton("Log Out")
        logout_button.setFixedSize(60, 25)
        logout_button.clicked.connect(self.logout.emit)

        top_layout.addWidget(help_button)
        top_layout.addWidget(logout_button)

        # Place the top-right widget using absolute positioning
        self.top_right_widget.setFixedHeight(30)
        self.top_right_widget.move(self.width() - self.top_right_widget.width() - 10, 10)
        self.top_right_widget.setParent(self)
        self.top_right_widget.show()

        self.setLayout(root_layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.top_right_widget.move(self.width() - self.top_right_widget.width() - 10, 10)