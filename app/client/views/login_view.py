from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtCore import Qt


class LoginView(QWidget):
    def __init__(self):
        super().__init__()
        self._build_ui()

    def _build_ui(self):
        # Root layout
        root_layout = QVBoxLayout()
        root_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root_layout.setSpacing(20)

        # Title
        title = QLabel("SF6 Fantasy League")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            """
            QLabel {
                font-size: 28px;
                font-weight: bold;
            }
            """
        )

        # Subtitle
        subtitle = QLabel("Login")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet(
            """
            QLabel {
                font-size: 16px;
                color: #666666;
            }
            """
        )

        # Email field
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.setFixedHeight(36)

        # Password field
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(36)

        # Submit button
        self.submit_button = QPushButton("Login")
        self.submit_button.setFixedHeight(40)
        self.submit_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.submit_button.setStyleSheet(
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

        # Form container (controls width for aesthetics)
        form_layout = QVBoxLayout()
        form_layout.setSpacing(12)
        form_layout.addWidget(self.email_input)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.submit_button)

        form_container = QWidget()
        form_container.setLayout(form_layout)
        form_container.setFixedWidth(320)

        # Assemble layout
        root_layout.addWidget(title)
        root_layout.addWidget(subtitle)
        root_layout.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed))
        root_layout.addWidget(form_container)

        self.setLayout(root_layout)