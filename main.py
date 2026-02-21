import sys
from os import getcwd
from PyQt5.QtWidgets import QApplication
from desktop.app import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow(getcwd())
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
