from PyQt6.QtWidgets import QApplication, QMainWindow
from view import Ui_MainWindow
from controller import Controller
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    controller = Controller(ui)
    window.show()
    sys.exit(app.exec())