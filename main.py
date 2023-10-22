import sys

from player import MyPlayer
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyPlayer()
    ex.show()
    sys.exit(app.exec_())
