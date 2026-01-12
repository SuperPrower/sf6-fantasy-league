from PyQt6.QtWidgets import QMainWindow, QWidget
from PyQt6.QtCore import Qt
from app.client.views.login_view import LoginView


class FantasyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SF6 Fantasy League")
        self.resize(800, 600)

        # Set LoginView as the central widget
        self.login_view = LoginView()
        self.setCentralWidget(self.login_view)