import sys

from PyQt5.QtWidgets import (
    QApplication,
    QFrame
)

from PyQt5.QtGui import (
    QIcon
)

from os.path import (
    dirname,
    join,
    abspath
)
from os import (
    getcwd
)

from PyQt5.uic import loadUi

# Mine Modules
from modules.exelOptions import (
    loadExel,
    saveExel
)
from server.main_server import (
    MainServer
)

class MainWindow(QFrame):
    
    def __init__(self):
        
        super().__init__()
        
        self.initComponents()
        
        loadUi(self.pathUIface, self)
        
        self.setWindowTitle("Shedule Wallpaper")

        self.configComponents()

        self.setStyles()
        
    def initComponents(self):
        
        # self.full_path = join(dirname(abspath(__file__)))
        self.full_path = join(getcwd())
        
        self.pathFileExel = join(self.full_path, "src", "documents", "Horario.xlsx")
        
        self.server = MainServer(self.full_path)
        
        self.pathUIface = join(self.full_path, "interface", "Panel_UI.ui")
        
        path_icons = join(self.full_path, "src", "images")
        window_icon = QIcon(join(path_icons, "home.png"))
        
        self.setWindowIcon(window_icon)
        
        
    def configComponents(self):
        
        self.btnConfig.clicked.connect(self.startLoadExcel)
        
        self.btnSave.clicked.connect(self.startSaveExcel)
        
        self.btn_start_server.clicked.connect(self.initServer)
        
    def initServer(self):
        self.server.initServer()
        # self.server.initServer(self.full_path)

    def startLoadExcel(self):
        loadExel(self.tableExel, self.pathFileExel)
        
    def startSaveExcel(self):
        saveExel(self.tableExel, self.pathFileExel, self.full_path)

    def setStyles(self):
        style_path = join(self.full_path, "interface", "styles", "style_panel.css")
        try:
            file = open(style_path, "r").read()
            self.setStyleSheet(file)
        except FileNotFoundError:
            print("ERROR")
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
