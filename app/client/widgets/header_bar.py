from PyQt6.QtWidgets import (
    QWidget, 
    QHBoxLayout, 
    QPushButton, 
    QLabel,
)

from PyQt6.QtCore import Qt

from app.client.controllers.session import Session

class HeaderBar(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self._build_ui()

    def _build_ui(self):
        self.setFixedHeight(40)

        # create layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(10)

        # banner created when there's a message to display
        if Session.banner_message != None:
            self.banner_label = QLabel(Session.banner_message)
            self.banner_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            self.banner_label.setStyleSheet("""
                QLabel {
                    font-size: 12px;
                    background-color: #9ccfff;
                    color: #1661a8;
                    padding-left: 10px;
                    padding-right: 10px;
                }
            """)

            layout.addWidget(self.banner_label)

        else:
            layout.addStretch()

        # profile button
        self.popup = QLabel(
            "<b>Profile Info</b><br>"
            f"User: {Session.user}<br>"
            f"User ID: {Session.user_id}"
        )
        self.popup.setWindowFlags(Qt.WindowType.ToolTip)
        self.popup.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.popup.setStyleSheet("""
            background: #f5f5f5;
            border: 1px solid #aaa;
            padding: 6px;
        """)
        self.popup.hide()

        def show_popup():
            if self.popup.isVisible():
                self.popup.hide()
            else:
                pos = profile_button.mapToGlobal(
                    profile_button.rect().bottomRight()
                )
                self.popup.move(pos)
                self.popup.show()

        profile_button = QPushButton("Profile")
        profile_button.setCursor(Qt.CursorShape.PointingHandCursor)
        profile_button.clicked.connect(show_popup)

        # help and logout button
        help_button = QPushButton("Help")
        help_button.setCursor(Qt.CursorShape.PointingHandCursor)
        help_button.clicked.connect(self.app.open_help)

        logout_button = QPushButton("Log out")
        logout_button.setCursor(Qt.CursorShape.PointingHandCursor)
        logout_button.clicked.connect(self.app.logout)

        for btn in (help_button, logout_button, profile_button):
            btn.setFixedHeight(32)
            btn.setFixedWidth(64)

        profile_button.setStyleSheet("""
            QPushButton {
                font-size: 12px;
                background-color: #ffffff;
                color: #000000;
                border: none;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)

        help_button.setStyleSheet("""
            QPushButton {
                font-size: 12px;
                background-color: #ffffff;
                color: #000000;
                border: none;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)

        logout_button.setStyleSheet("""
            QPushButton {
                font-size: 12px;
                background-color: #a80000;
                color: #ffffff;
                border: none;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)

        layout.addWidget(profile_button)
        layout.addWidget(help_button)
        layout.addWidget(logout_button)