from pathlib import Path
import sys

from PyQt6.QtWidgets import (
    QWidget, 
    QLabel,
    QVBoxLayout, 
    QHBoxLayout,
    QFrame,
    QSizePolicy,
    QScrollArea,
    QPushButton,
    QApplication
)

from PyQt6.QtCore import Qt

from PyQt6.QtGui import QPixmap

from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QGridLayout, QGroupBox, QPushButton, QScrollArea
)
from PyQt6.QtCore import Qt

from app.client.controllers.session import Session

from app.client.widgets.header_bar import HeaderBar
from app.client.widgets.footer_nav import FooterNav

from app.client.theme import *

class GlobalView(QWidget):

    def __init__(self, app):
        super().__init__()
        self.app = app

        # root layout: defined here to use in other private methods
        self.root_layout = QVBoxLayout()
        self.root_layout.setContentsMargins(0, 0, 0, 0)
        self.root_layout.setSpacing(0)
        self.setLayout(self.root_layout)

        # grab player info from cache
        self.global_stats = Session.global_stats or []

        self._build_main()


    def _build_main(self):
        self.root_layout.addWidget(HeaderBar(self.app))

        # main content
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        content_layout.setContentsMargins(50, 35, 50, 35)
        content_layout.setSpacing(10)

        # scrollable if required
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet(SCROLL_STYLESHEET)
        scroll.setWidget(content_widget)

        # composing content
        content_layout.addWidget(self._build_title())
        if bool(self.global_stats):
            content_layout.addWidget(self._build_stats(self.global_stats[0]))

        # composing root
        self.root_layout.addWidget(scroll, stretch=1)
        self.root_layout.addWidget(FooterNav(self.app))

    def _build_title(self):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setSpacing(20)

        players = QPushButton("Player Pool")
        players.setCursor(Qt.CursorShape.PointingHandCursor)
        players.clicked.connect(self.app.show_players_view)
        players.setStyleSheet(BUTTON_STYLESHEET_A)

        globals_btn = QPushButton("Global Stats")
        globals_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        globals_btn.clicked.connect(self.app.show_globals_view)
        globals_btn.setStyleSheet(BUTTON_STYLESHEET_A)

        global_stats = QLabel("Global Stats")
        global_stats.setAlignment(Qt.AlignmentFlag.AlignCenter)
        global_stats.setStyleSheet("""
            font-size: 64px; 
            font-weight: bold;
        """)

        left = QWidget()
        center = QWidget()
        right = QWidget()

        center_layout = QHBoxLayout(center)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.addWidget(global_stats, alignment=Qt.AlignmentFlag.AlignCenter)

        right_layout = QHBoxLayout(right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.addStretch()
        right_layout.addWidget(players, alignment=Qt.AlignmentFlag.AlignTop)

        left_layout = QHBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.addWidget(globals_btn, alignment=Qt.AlignmentFlag.AlignTop)
        left_layout.addStretch()

        layout.addWidget(left, 1)
        layout.addWidget(center)
        layout.addWidget(right, 1)

        return container

    def _build_stats(self, stats: dict) -> QWidget:
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # ensures everything stacks from top

        def add_row(grid, row_idx, name, value):
            grid.addWidget(QLabel(name, alignment=Qt.AlignmentFlag.AlignLeft), row_idx, 0)
            grid.addWidget(QLabel(value, alignment=Qt.AlignmentFlag.AlignRight), row_idx, 1)

        # Main stats grid
        main_grid = QGridLayout()
        main_grid.setHorizontalSpacing(20)
        main_grid.setVerticalSpacing(5)
        row = 0

        add_row(main_grid, row, "Managers Count", str(stats.get("managers_count", 0)))
        row += 1
        add_row(main_grid, row, "Leagues Count", str(stats.get("leagues_count", 0)))
        row += 1

        best_team = stats.get("best_scoring_team", {})
        add_row(main_grid, row, "Best Scoring Team",
                f"{best_team.get('team_name','-')} ({best_team.get('total_points',0)} pts)")
        row += 1
        add_row(main_grid, row, "Unique Players Picked", str(stats.get("unique_players_picked", 0)))
        row += 1
        add_row(main_grid, row, "Tier Whore Teams", str(stats.get("tier_whore", {}).get("count", 0)))
        row += 1

        layout.addLayout(main_grid)

        # Collapsible sections helper
        def add_collapsible_section(title: str, items: list, formatter=lambda x: str(x)):
            group = QGroupBox(title)
            group.setCheckable(True)
            group.setChecked(False)  # collapsed by default
            group_layout = QVBoxLayout(group)
            for item in items:
                group_layout.addWidget(QLabel(formatter(item)))
            layout.addWidget(group)

        # Players by region
        regions = stats.get("players_by_region", [])
        add_collapsible_section(
            "Players by Region",
            regions,
            lambda r: f"{r.get('region','Unknown')}: {r.get('player_count',0)} players, "
                    f"{r.get('total_points',0)} pts, avg {r.get('avg_points',0):.1f}"
        )

        # Most picked players
        most_picked = stats.get("most_picked_players", [])
        add_collapsible_section(
            "Most Picked Players",
            most_picked,
            lambda p: f"{p['player_name']} ({p['pick_count']} picks)"
        )

        # Least picked players
        least_picked = stats.get("least_picked_players", [])
        add_collapsible_section(
            "Least Picked Players",
            least_picked,
            lambda p: f"{p['player_name']} ({p['pick_count']} picks)"
        )

        # Pickrate / points ratio
        ratio_stats = stats.get("pickrate_points_ratio", {})
        ratio_texts = []
        lpmp = ratio_stats.get("lowest_pickrate_most_points", {})
        hlrp = ratio_stats.get("highest_pickrate_least_points", {})
        ratio_texts.append(f"Lowest Pickrate / Most Points: {lpmp.get('player_name','-')} ({lpmp.get('ratio','-')})")
        ratio_texts.append(f"Highest Pickrate / Least Points: {hlrp.get('player_name','-')} ({hlrp.get('ratio','-')})")
        add_collapsible_section("Pickrate / Points Ratio", ratio_texts)

        return container  # no scroll, the outer scroll handles it