from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
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

    def __init__(self):
        super().__init__()
        self._build_ui()

    def _build_ui(self):
        root_layout = QVBoxLayout()
        root_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root_layout.setSpacing(20)

        # ----- Title -----
        title = QLabel("Home")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            """
            QLabel {
                font-size: 26px;
                font-weight: bold;
            }
            """
        )

        # ----- User info -----
        username = Session.user or "Player"

        user_label = QLabel(f"Welcome, {username}")
        user_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        user_label.setStyleSheet(
            """
            QLabel {
                font-size: 16px;
                color: #555555;
            }
            """
        )

        # Placeholder league/team info
        league_info = QLabel("Current League: Not selected")
        team_info = QLabel("Current Team: Not selected")

        for label in (league_info, team_info):
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet(
                """
                QLabel {
                    font-size: 14px;
                    color: #666666;
                }
                """
            )

        # ----- Buttons -----
        league_button = QPushButton("Go to League")
        team_button = QPushButton("Go to Team")
        player_button = QPushButton("View Players")
        leaderboard_button = QPushButton("View Leaderboards")

        for button in (league_button, team_button, leaderboard_button, player_button):
            button.setFixedHeight(42)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setStyleSheet(
                """
                QPushButton {
                    font-size: 14px;
                    font-weight: bold;
                    background-color: #2d7df6;
                    color: white;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #1f6ae1;
                }
                QPushButton:pressed {
                    background-color: #1a5bc4;
                }
                """
            )

        # ----- Wire signals -----
        league_button.clicked.connect(self.open_league_view.emit)
        team_button.clicked.connect(self.open_team_view.emit)
        leaderboard_button.clicked.connect(self.open_leaderboards.emit)
        player_button.clicked.connect(self.open_players.emit)

        # ----- Assemble layout -----
        root_layout.addWidget(title)
        root_layout.addWidget(user_label)
        root_layout.addSpacing(10)
        root_layout.addWidget(league_info)
        root_layout.addWidget(team_info)
        root_layout.addSpacing(20)
        root_layout.addWidget(league_button)
        root_layout.addWidget(team_button)
        root_layout.addWidget(player_button)
        root_layout.addWidget(leaderboard_button)

        self.setLayout(root_layout)