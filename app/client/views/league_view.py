from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QGroupBox
)
from PyQt6.QtCore import pyqtSignal, Qt
from app.client.session import Session

class LeagueView(QWidget):
    back_to_home = pyqtSignal()

    def __init__(self, app):
        super().__init__()
        self.app = app
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(15)

        # ----- User's current league info -----
        league_name = Session.current_league_name or "None"
        league_id = Session.current_league_id or "N/A"
        self.league_info_label = QLabel(f"Current League: {league_name} (ID: {league_id})")
        self.league_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.league_info_label.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: #333;"
        )
        self.league_info_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        layout.addWidget(self.league_info_label)

        # ----- Create League -----
        create_group = QGroupBox("Create League")
        create_layout = QHBoxLayout()
        self.create_input = QLineEdit()
        self.create_input.setPlaceholderText("League Name")
        create_btn = QPushButton("Create")
        create_btn.clicked.connect(self.create_league)
        create_layout.addWidget(self.create_input)
        create_layout.addWidget(create_btn)
        create_group.setLayout(create_layout)
        layout.addWidget(create_group)

        # ----- Join League -----
        join_group = QGroupBox("Join League")
        join_layout = QHBoxLayout()
        self.join_input = QLineEdit()
        self.join_input.setPlaceholderText("League ID")
        join_btn = QPushButton("Join")
        join_btn.clicked.connect(self.join_league)
        join_layout.addWidget(self.join_input)
        join_layout.addWidget(join_btn)
        join_group.setLayout(join_layout)
        layout.addWidget(join_group)

        # ----- Leave League -----
        leave_btn = QPushButton("Leave League")
        leave_btn.clicked.connect(self.leave_league)
        layout.addWidget(leave_btn)

        # ----- Assign Draft Order -----
        draft_order_btn = QPushButton("Assign Draft Order")
        draft_order_btn.clicked.connect(self.assign_draft_order)
        layout.addWidget(draft_order_btn)

        # ----- Begin Draft -----
        begin_draft_btn = QPushButton("Begin Draft")
        begin_draft_btn.clicked.connect(self.begin_draft)
        layout.addWidget(begin_draft_btn)

        # ----- Set Forfeit -----
        forfeit_btn = QPushButton("Set Forfeit")
        forfeit_btn.clicked.connect(self.set_forfeit)
        layout.addWidget(forfeit_btn)

        # ----- Back to Home -----
        back_btn = QPushButton("Back to Home")
        back_btn.clicked.connect(lambda: self.back_to_home.emit())
        layout.addWidget(back_btn)

        # ----- Status label -----
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
        QLabel {
            font-size: 12px;
            color: #cc0000;
        }
        """)
        layout.addWidget(self.status_label)

        # Set layout
        self.setLayout(layout)

    # ----- Slots wired to LeagueService -----
    def create_league(self):
        name = self.create_input.text().strip()
        if not name:
            self.status_label.setText("Please enter a league name.")
            return
        try:
            success = Session.league_service.create_then_join_league(name)
            if success:
                Session.current_league_name = name
                Session.current_league_id = success
                self.league_info_label.setText(
                    f"Current League: {name} (ID: {Session.current_league_id})"
                )
                self.status_label.setText(f"League '{name}' created successfully!")
                self.status_label.setStyleSheet("color: #2e7d32;")
        except Exception as e:
            self.status_label.setText(f"Failed to create league: {e}")
            self.status_label.setStyleSheet("color: #cc0000;")

    def join_league(self):
        league_id = self.join_input.text().strip()
        if not league_id:
            self.status_label.setText("Please enter a league ID.")
            return
        try:
            success = Session.league_service.join_league(league_id)
            if success:
                Session.init_aesthetics()
                self.league_info_label.setText(
                    f"Current League: {Session.current_league_name} (ID: {Session.current_league_id})"
                )
                self.status_label.setText(f"Successfully joined league {league_id}!")
                self.status_label.setStyleSheet("color: #2e7d32;")
        except Exception as e:
            self.status_label.setText(f"Failed to join league: {e}")
            self.status_label.setStyleSheet("color: #cc0000;")

    def leave_league(self):
        try:
            success = Session.league_service.leave_league()
            if success:
                Session.current_league_name = None
                Session.current_league_id = None
                self.league_info_label.setText("Current League: None (ID: N/A)")
                self.status_label.setText("You have left the league successfully.")
                self.status_label.setStyleSheet("color: #2e7d32;")
        except Exception as e:
            self.status_label.setText(f"Failed to leave league: {e}")
            self.status_label.setStyleSheet("color: #cc0000;")

    def assign_draft_order(self):
        try:
            # Example placeholder: pull usernames from Session or backend
            ordered_usernames = ["user1", "user2"]  # Replace with real data
            success = Session.league_service.assign_draft_order(ordered_usernames)
            if success:
                self.status_label.setText("Draft order assigned successfully!")
                self.status_label.setStyleSheet("color: #2e7d32;")
        except Exception as e:
            self.status_label.setText(f"Failed to assign draft order: {e}")
            self.status_label.setStyleSheet("color: #cc0000;")

    def begin_draft(self):
        try:
            success = Session.league_service.begin_draft()
            if success:
                self.status_label.setText("Draft has begun!")
                self.status_label.setStyleSheet("color: #2e7d32;")
        except Exception as e:
            self.status_label.setText(f"Failed to begin draft: {e}")
            self.status_label.setStyleSheet("color: #cc0000;")

    def set_forfeit(self):
        try:
            # Example placeholder: user input or predefined value
            forfeit_text = "Forfeit Example"  # You can replace with QLineEdit input
            success = Session.league_service.set_forfeit(forfeit_text)
            if success:
                self.status_label.setText(f"Forfeit set: {forfeit_text}")
                self.status_label.setStyleSheet("color: #2e7d32;")
        except Exception as e:
            self.status_label.setText(f"Failed to set forfeit: {e}")
            self.status_label.setStyleSheet("color: #cc0000;")