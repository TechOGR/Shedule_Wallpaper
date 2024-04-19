from PyQt5.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QDialog
)
from PyQt5.QtCore import (
    Qt
)
from PyQt5.QtGui import (
    QIcon
)

from os.path import (
    join
)

class Dialog(QDialog):
    
    def __init__(self, texto, main_path):
        super().__init__()
        
        path_icon = join(main_path, "src", "images", "home.png")
        window_icon = QIcon(path_icon)
        
        self.setWindowTitle("Information")
        self.setFixedSize(200,100)
        self.setStyleSheet("background-color: black;")
        self.setVisible(True)
        self.setWindowIcon(window_icon)
        
        label = QLabel("Hola", self)
        label.setStyleSheet("color: white; font-size: 16px;")
        label.setText(texto)
        label.setAlignment(Qt.AlignCenter)
        
        layout = QVBoxLayout()
        layout.addWidget(label)
        
        self.setLayout(layout)
        