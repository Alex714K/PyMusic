from classes import Player
from PyQt5.QtWidgets import QApplication
from sys import argv


if __name__ == "__main__":
    import sys

app = QApplication(sys.argv)
application = Player()
application.show()
sys.exit(app.exec())
