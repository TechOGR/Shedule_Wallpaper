import sys

from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
)

from PyQt5.QtGui import (
    QIcon,
    QPainter,
    QPainterPath,
    QRegion,
    QPixmap
)


from PyQt5.QtCore import (
    Qt,
)

from os.path import (
    join,
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
from modules.openSocials import (
    openLinks
)

class MainWindow(QFrame):
    
    def __init__(self):
        
        super().__init__()
        
        self.initComponents()
        
        loadUi(self.pathUIface, self)
        
        self.setWindowTitle("Shedule Wallpaper")

        self.configComponents()

        self.setStyles()
        
        self.setWindowFlag(Qt.FramelessWindowHint)
        
    def initComponents(self):
        
        # self.full_path = join(dirname(abspath(__file__)))
        self.full_path = join(getcwd())
        
        self.pathFileExel = join(self.full_path, "src", "documents", "Horario.xlsx")
        
        self.server = MainServer(self.full_path)
        
        self.pathUIface = join(self.full_path, "interface", "Panel_UI.ui")
        
        self.path_icons = join(self.full_path, "src", "images")
        window_icon = QIcon(join(self.path_icons, "logo_wall.png"))
        
        self.setWindowIcon(window_icon)
        
        
    def configComponents(self):
        
        self.btnConfig.clicked.connect(self.startLoadExcel)
        
        self.btnSave.clicked.connect(self.startSaveExcel)
        
        self.btn_start_server.clicked.connect(self.initServer)
        self.btn_stop_server.clicked.connect(self.stopServer)
        
        
        styleButtonExit =  """
                background-color: red;
                border-radius: 10px; 
                border: none;
                color: black;
                font-size: 18px;
                font-weight: bold;
                width: 50px;
                height: 50px;
                padding: 0;
            """
        styleButtonMinimize =  """
                background-color: yellow;
                border-radius: 10px; 
                border: none;
                color: black;
                font-size: 20px;
                font-weight: bold;
                width: 50px;
                height: 50px;
                padding: 0;
            """
        self.btn_exit.setStyleSheet(styleButtonExit)
        self.btn_minimize.setStyleSheet(styleButtonMinimize)
        self.btn_exit.clicked.connect(self.functionExit)
        self.btn_minimize.clicked.connect(self.functionMinimize)
        
        iconLabelTopLeft = QPixmap(50,50)
        iconLabelTopLeft.load(join(self.path_icons, "min_size_logo.png"))
        self.label_icon_app.setPixmap(iconLabelTopLeft)
        
        self.btn_youtube.clicked.connect(self.openSocials)
        
    def openSocials(self):
        if self.btn_youtube.isChecked():
            openLinks('youtube')
        
    def functionExit(self):
        self.close()
        sys.exit(0)
        
    def functionMinimize(self):
        self.showMinimized()
        
    def initServer(self):
        self.server.initServer()
        # self.server.initServer(self.full_path)

    def stopServer(self):
        self.server.stopServer()

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
            
    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Escape:
            self.close()
            sys.exit(0)
            
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
            
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()
            
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.width(), self.height(), 10, 10)
        
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
