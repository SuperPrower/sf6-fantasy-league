from pathlib import Path

from datetime import datetime

from PyQt6.QtWidgets import (
    QWidget, 
    QLabel, 
    QPushButton, 
    QVBoxLayout, 
    QHBoxLayout, 
    QComboBox,
    QLineEdit,
    QGroupBox,
    QFrame,
    QSizePolicy,
    QScrollArea,
)

from PyQt6.QtCore import Qt

from PyQt6.QtGui import QPixmap

from app.client.controllers.session import Session
from app.client.controllers.async_runner import run_async

from app.client.widgets.header_bar import HeaderBar
from app.client.widgets.footer_nav import FooterNav

class LeaderboardView(QWidget):

    def __init__(self, app):
        super().__init__()
        self.app = app

        # root layout: defined here to use in other private methods
        self.root_layout = QVBoxLayout()
        self.root_layout.setContentsMargins(0, 0, 0, 0)
        self.root_layout.setSpacing(0)
        self.setLayout(self.root_layout)

        # clears then builds ui
        self._refresh_view()


    def _build_main(self):
        self.root_layout.addWidget(HeaderBar(self.app))

        # grabbing cached data
        self.username = Session.user
        self.user_id = Session.user_id
        self.team_name = Session.current_team_name
        self.next_pick = Session.next_pick
        self.draft_complete = Session.draft_complete
        self.my_team_data = Session.my_team_data


        # main content
        self.content_widget = QWidget()

        content_layout = QVBoxLayout(self.content_widget)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        content_layout.setContentsMargins(50, 35, 50, 35)
        content_layout.setSpacing(35)


        # adding layouts to main content
        # ---

        # scrollable if required
        scrollable = QScrollArea()
        scrollable.setWidgetResizable(True)
        scrollable.setWidget(self.content_widget)

        # composing root
        self.root_layout.addWidget(scrollable, stretch=1)
        self.root_layout.addWidget(FooterNav(self.app))


    def _build_info():
        pass
    
    def _build_league_teams():
        pass

    def _build_favourites():
        pass


    def _refresh_view(self):
        self._clear_layout(self.layout())
        Session.init_aesthetics()
        Session.init_leaderboards()
        self._build_main()

    def _clear_layout(self, layout):
        if layout is None:
            return

        while layout.count():
            item = layout.takeAt(0)

            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
                continue

            child_layout = item.layout()
            if child_layout is not None:
                self._clear_layout(child_layout)

    def _create_separator(self):
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("color: #7a7a7a;")
        separator.setFixedHeight(2)
        separator.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )
        return separator