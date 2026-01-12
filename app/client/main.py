import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from app.client.app import FantasyApp


def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("app/client/assets/icons/logo.png"))

    window = FantasyApp()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()