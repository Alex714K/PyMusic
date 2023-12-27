from Player import Player
from PyQt5.QtWidgets import QApplication
import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    application = Player()
    application.show()
    sys.exit(app.exec())
