import sys
import subprocess
import json

from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
    QGraphicsDropShadowEffect,
)

from PyQt5.QtGui import (
    QIcon,
    QPainter,
    QPainterPath,
    QRegion,
    QPixmap,
    QColor,
    QLinearGradient,
    QBrush,
)

from PyQt5.QtCore import (
    Qt,
)

from os.path import (
    join,
    exists,
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

CONFIG_URL = "http://localhost:5000/api/config"
AIMP_PATH = r"C:\Program Files\AIMP\AIMP.exe"


class MainWindow(QFrame):

    def __init__(self):
        super().__init__()

        self.initComponents()
        loadUi(self.pathUIface, self)

        self.setWindowTitle("Shedule Wallpaper")
        self.configComponents()
        self.setStyles()

        # Frameless + translucent for glass effect
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    # ── Init ──────────────────────────────────────────
    def initComponents(self):
        self.full_path = join(getcwd())

        self.pathFileExelA = join(self.full_path, "src", "documents", "Horario.xlsx")
        self.pathFileExelB = join(self.full_path, "src", "documents", "HorarioB.xlsx")
        self.activeWeek = "A"

        self.config_path = join(self.full_path, "src", "documents", "app_config.json")

        self.server = MainServer(self.full_path)

        self.pathUIface = join(self.full_path, "interface", "Panel_UI.ui")
        self.path_icons = join(self.full_path, "src", "images")
        self.setWindowIcon(QIcon(join(self.path_icons, "tiny_logo.png")))

    # ── Config ────────────────────────────────────────
    def configComponents(self):
        # Table buttons
        self.btnConfig.clicked.connect(self.startLoadExcel)
        self.btnSave.clicked.connect(self.startSaveExcel)

        # Server buttons
        self.btn_start_server.clicked.connect(self.initServer)
        self.btn_stop_server.clicked.connect(self.stopServer)

        # Window buttons
        self.btn_exit.clicked.connect(self.functionExit)
        self.btn_minimize.clicked.connect(self.functionMinimize)

        # App icon
        icon = QPixmap(50, 50)
        icon.load(join(self.path_icons, "min_size_logo.png"))
        self.label_icon_app.setPixmap(icon)

        # Socials
        self.btn_youtube.clicked.connect(lambda: openLinks('youtube'))
        self.btn_github.clicked.connect(lambda: openLinks('github'))
        self.btn_facebook.clicked.connect(lambda: openLinks('facebook'))
        self.btn_twitter.clicked.connect(lambda: openLinks('twitter'))
        self.btn_instagram.clicked.connect(lambda: openLinks('instagram'))

        # ── Checkboxes ────────────────────────────────
        self.check_blur_background.stateChanged.connect(self.onBlurChanged)
        self.check_trash.stateChanged.connect(self.onTrashChanged)
        self.check_player.stateChanged.connect(self.onMusicChanged)

        # ── Week radio buttons ────────────────────────
        self.week_a.setChecked(True)
        self.week_a.toggled.connect(self.onWeekChanged)

        # Load saved config into UI
        self._loadConfigToUI()

    # ── Config helpers ────────────────────────────────
    def _readConfig(self):
        if exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"blur": True, "trash": True, "music": False, "activeWeek": "A"}

    def _writeConfig(self, data):
        cfg = self._readConfig()
        cfg.update(data)
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)

    def _loadConfigToUI(self):
        cfg = self._readConfig()
        self.check_blur_background.setChecked(cfg.get("blur", True))
        self.check_trash.setChecked(cfg.get("trash", True))
        self.check_player.setChecked(cfg.get("music", False))
        if cfg.get("activeWeek", "A") == "B":
            self.week_b.setChecked(True)
            self.activeWeek = "B"
        else:
            self.week_a.setChecked(True)
            self.activeWeek = "A"

    # ── Checkbox handlers ─────────────────────────────
    def onBlurChanged(self, state):
        self._writeConfig({"blur": state == Qt.Checked})

    def onTrashChanged(self, state):
        self._writeConfig({"trash": state == Qt.Checked})

    def onMusicChanged(self, state):
        enabled = state == Qt.Checked
        self._writeConfig({"music": enabled})
        if enabled:
            self._openAIMP()
        else:
            self._closeAIMP()

    def onWeekChanged(self, checked):
        self.activeWeek = "A" if checked else "B"
        self._writeConfig({"activeWeek": self.activeWeek})

    def _openAIMP(self):
        try:
            if exists(AIMP_PATH):
                subprocess.Popen([AIMP_PATH], shell=False)
        except Exception as e:
            print(f"Could not open AIMP: {e}")

    def _closeAIMP(self):
        try:
            subprocess.run(["taskkill", "/F", "/IM", "AIMP.exe"],
                           capture_output=True, shell=False)
        except Exception:
            pass

    # ── Window controls ───────────────────────────────
    def functionExit(self):
        self.close()
        sys.exit(0)

    def functionMinimize(self):
        self.showMinimized()

    # ── Server ────────────────────────────────────────
    def initServer(self):
        self.server.initServer()

    def stopServer(self):
        self.server.stopServer()

    # ── Excel ─────────────────────────────────────────
    def startLoadExcel(self):
        path = self.pathFileExelA if self.activeWeek == "A" else self.pathFileExelB
        loadExel(self.tableExel, path)

    def startSaveExcel(self):
        path = self.pathFileExelA if self.activeWeek == "A" else self.pathFileExelB
        saveExel(self.tableExel, path, self.full_path)

    # ── Styles ────────────────────────────────────────
    def setStyles(self):
        style_path = join(self.full_path, "interface", "styles", "style_panel.css")
        try:
            with open(style_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Style file not found")

    # ── Events ────────────────────────────────────────
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
        path.addRoundedRect(0, 0, self.width(), self.height(), 16, 16)

        # Glass background gradient
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor(30, 30, 50, 200))
        gradient.setColorAt(0.5, QColor(20, 20, 40, 210))
        gradient.setColorAt(1.0, QColor(15, 15, 30, 220))

        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawPath(path)

        # Subtle top highlight
        highlight = QPainterPath()
        highlight.addRoundedRect(1, 1, self.width() - 2, 60, 16, 16)
        painter.setBrush(QColor(255, 255, 255, 8))
        painter.drawPath(highlight)

        # Rounded mask
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
