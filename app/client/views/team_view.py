from PyQt6.QtWidgets import (
    QWidget, 
    QLabel, 
    QPushButton, 
    QVBoxLayout, 
    QHBoxLayout, 
    QLineEdit, 
    QGroupBox,
    QFrame,
    QSizePolicy,
    QScrollArea
)

from PyQt6.QtCore import Qt

from app.client.controllers.session import Session
from app.client.controllers.async_runner import run_async

from app.client.widgets.header_bar import HeaderBar
from app.client.widgets.footer_nav import FooterNav

class TeamView(QWidget):

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

        # main content
        self.content_widget = QWidget()

        content_layout = QVBoxLayout(self.content_widget)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        content_layout.setContentsMargins(50, 35, 50, 35)
        content_layout.setSpacing(35)

        # status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #cc0000;
            }
        """)

        # adding layouts to main content
        content_layout.addWidget(self._build_my_info())
        content_layout.addWidget(self._create_separator())

        if self.next_pick == self.username and self.draft_complete == False:
            content_layout.addWidget(self._build_draft_pick())
            content_layout.addWidget(self._create_separator())


        # scrollable if required
        scrollable = QScrollArea()
        scrollable.setWidgetResizable(True)
        scrollable.setWidget(self.content_widget)

        # composing root
        self.root_layout.addWidget(scrollable, stretch=1)
        self.root_layout.addWidget(FooterNav(self.app))


    def _build_my_info(self):
        info_cont = QWidget()
        info_layout = QVBoxLayout(info_cont)
        info_layout.setSpacing(10)
        info_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        team_label = QLabel(f"{self.team_name}")
        team_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        team_label.setStyleSheet("""
            font-size: 48px; 
            font-weight: bold; 
            color: #333; 
        """)

        info_layout.addWidget(team_label)
        info_layout.addWidget(self.status_label)

        return info_cont

    def _build_draft_pick(self):
        pick_cont = QWidget()

        main_layout = QVBoxLayout(pick_cont)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.pick_input = QLineEdit()
        self.pick_input.setPlaceholderText("Blaz, MenaRD, Leshar...")

        pick_group_layout = QVBoxLayout()
        pick_group_layout.addWidget(self.pick_input)

        pick_group = QGroupBox("Pick a Player!")
        pick_group.setLayout(pick_group_layout)

        pick_label = QLabel("It's your turn to pick a player!")
        pick_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pick_label.setStyleSheet("""
            font-size: 24px; 
            font-weight: bold; 
            color: #333; 
        """)

        pick_btn = QPushButton("Pick")
        pick_btn.setFixedWidth(100)
        pick_btn.setFixedHeight(30)
        pick_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        pick_btn.setStyleSheet("""
            QPushButton {
                font-size: 12px;
                background-color: #ff9d00;
                color: #000000;
            }
            QPushButton:hover {
                background-color: #ffaa22;
            }
            QPushButton:pressed {
                background-color: #de8900;
            }
        """)
        pick_btn.clicked.connect(self.pick_player)

        pick_layout = QHBoxLayout()
        pick_layout.addWidget(pick_group)
        pick_layout.addWidget(pick_btn)
        pick_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout.addWidget(pick_label)
        main_layout.addLayout(pick_layout)
        
        return pick_cont
    
    def _build_my_team(self):
        pass

    def _build_player_stat_list(self):
        pass


    def pick_player(self):
        player = self.pick_input.text().strip()
        print("pick_player: CLICK")

        if not player:
            self._set_status("Please enter a player name.", status_type="e")
            return
        
        if not any(p["name"] == player for p in Session.player_scores):
            self._set_status(f"{player} not found. Names are case sensitive!", status_type="e")
            return
        
        def _success(success):
            if success:
                self._refresh_view()
                self._set_status(f"Welcome {player} to {self.team_name}!", status_type="s")
        
        def _error(error):
            self._set_status(f"Failed to pick player: {error}", status_type="e")
        
        self._set_status("Picking player...", status_type="p")
        run_async(
            parent_widget= self.content_widget,
            fn= Session.team_service.pick_player,
            args= (player,),
            on_success=_success,
            on_error=_error
        )


    def _refresh_view(self):
        self._clear_layout(self.layout())
        Session.init_aesthetics()
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

    def _set_status(self, msg, status_type):
        self.status_label.setText(msg)

        if status_type == "s":
            color = "#2e7d32"
        elif status_type == "e":
            color = "#cc0000"
        else:
            color = "#333333"

        self.status_label.setStyleSheet(f"color: {color};")