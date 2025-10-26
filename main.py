import sys

from PyQt6.QtWidgets import QApplication

from ui.main_window import MainWindow


def main() -> None:
    app: QApplication = QApplication(sys.argv)
    window: MainWindow = MainWindow()
    window.showFullScreen()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
