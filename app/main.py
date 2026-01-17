import sys

from pathlib import Path

from PyQt6.QtWidgets import QApplication

from PyQt6.QtGui import QIcon

from PyQt6.QtCore import QLockFile

from app.client.app import FantasyApp

APP_NAME = "SF6FantasyLeague"

def main():
    appdata_dir = Path.home() / "AppData" / "Roaming" / APP_NAME
    appdata_dir.mkdir(parents=True, exist_ok=True)

    # creating lock file
    lock_file_path = appdata_dir / "app.lock"
    lock = QLockFile(str(lock_file_path))
    lock.setStaleLockTime(0)

    if not lock.tryLock():
        sys.exit(0)

    app = QApplication(sys.argv)

    app.setWindowIcon(
        QIcon(
            str(resource_path("app/client/assets/icons/logo.png"))
        )
    )

    window = FantasyApp()
    window.show()

    sys.exit(app.exec())

def resource_path(relative: str) -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS) / relative
    return Path(relative)

if __name__ == "__main__":
    main()