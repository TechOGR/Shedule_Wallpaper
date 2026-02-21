import sys
import subprocess
import json

from PyQt5.QtWidgets import QApplication, QFrame
from PyQt5.QtGui import (
    QIcon, QPainter, QPainterPath, QRegion,
    QPixmap, QColor, QLinearGradient, QBrush,
)
from PyQt5.QtCore import Qt
from os.path import join, exists
from PyQt5.uic import loadUi

from desktop.modules.excel import load_excel, save_excel
from desktop.modules.socials import open_link
from server.app import MainServer

AIMP_PATH = r"C:\Program Files\AIMP\AIMP.exe"


class MainWindow(QFrame):

    def __init__(self, base_path):
        super().__init__()

        self.full_path = base_path
        self.init_paths()
        loadUi(self.path_ui, self)

        self.setWindowTitle("Schedule Wallpaper")
        self.config_components()
        self.set_styles()

        # Frameless + translucent for glass effect
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    # ── Paths ──────────────────────────────────────────
    def init_paths(self):
        self.path_excel_a = join(self.full_path, "data", "documents", "Horario.xlsx")
        self.path_excel_b = join(self.full_path, "data", "documents", "HorarioB.xlsx")
        self.active_week = "A"

        self.config_path = join(self.full_path, "data", "documents", "app_config.json")

        self.server = MainServer(self.full_path)

        self.path_ui = join(self.full_path, "desktop", "ui", "panel.ui")
        self.path_icons = join(self.full_path, "data", "images")
        self.setWindowIcon(QIcon(join(self.path_icons, "tiny_logo.png")))

    # ── Components ─────────────────────────────────────
    def config_components(self):
        # Table buttons
        self.btnConfig.clicked.connect(self.start_load_excel)
        self.btnSave.clicked.connect(self.start_save_excel)

        # Server buttons
        self.btn_start_server.clicked.connect(self.init_server)
        self.btn_stop_server.clicked.connect(self.stop_server)

        # Window buttons
        self.btn_exit.clicked.connect(self.function_exit)
        self.btn_minimize.clicked.connect(self.function_minimize)

        # App icon
        icon = QPixmap(50, 50)
        icon.load(join(self.path_icons, "min_size_logo.png"))
        self.label_icon_app.setPixmap(icon)

        # Socials
        self.btn_youtube.clicked.connect(lambda: open_link('youtube'))
        self.btn_github.clicked.connect(lambda: open_link('github'))
        self.btn_facebook.clicked.connect(lambda: open_link('facebook'))
        self.btn_twitter.clicked.connect(lambda: open_link('twitter'))
        self.btn_instagram.clicked.connect(lambda: open_link('instagram'))

        # Checkboxes
        self.check_blur_background.stateChanged.connect(self.on_blur_changed)
        self.check_trash.stateChanged.connect(self.on_trash_changed)
        self.check_player.stateChanged.connect(self.on_music_changed)

        # Week radio buttons
        self.week_a.setChecked(True)
        self.week_a.toggled.connect(self.on_week_changed)

        # Load saved config into UI
        self._load_config_to_ui()

    # ── Config helpers ─────────────────────────────────
    def _read_config(self):
        if exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"blur": True, "trash": True, "music": False, "activeWeek": "A"}

    def _write_config(self, data):
        cfg = self._read_config()
        cfg.update(data)
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)

    def _load_config_to_ui(self):
        cfg = self._read_config()
        self.check_blur_background.setChecked(cfg.get("blur", True))
        self.check_trash.setChecked(cfg.get("trash", True))
        self.check_player.setChecked(cfg.get("music", False))
        if cfg.get("activeWeek", "A") == "B":
            self.week_b.setChecked(True)
            self.active_week = "B"
        else:
            self.week_a.setChecked(True)
            self.active_week = "A"

    # ── Checkbox handlers ──────────────────────────────
    def on_blur_changed(self, state):
        self._write_config({"blur": state == Qt.Checked})

    def on_trash_changed(self, state):
        self._write_config({"trash": state == Qt.Checked})

    def on_music_changed(self, state):
        enabled = state == Qt.Checked
        self._write_config({"music": enabled})
        if enabled:
            self._open_aimp()
        else:
            self._close_aimp()

    def on_week_changed(self, checked):
        self.active_week = "A" if checked else "B"
        self._write_config({"activeWeek": self.active_week})

    def _open_aimp(self):
        try:
            if exists(AIMP_PATH):
                subprocess.Popen([AIMP_PATH], shell=False)
        except Exception as e:
            print(f"Could not open AIMP: {e}")

    def _close_aimp(self):
        try:
            subprocess.run(
                ["taskkill", "/F", "/IM", "AIMP.exe"],
                capture_output=True, shell=False
            )
        except Exception:
            pass

    # ── Window controls ────────────────────────────────
    def function_exit(self):
        self.close()
        sys.exit(0)

    def function_minimize(self):
        self.showMinimized()

    # ── Server ─────────────────────────────────────────
    def init_server(self):
        self.server.init_server()

    def stop_server(self):
        self.server.stop_server()

    # ── Excel ──────────────────────────────────────────
    def start_load_excel(self):
        path = self.path_excel_a if self.active_week == "A" else self.path_excel_b
        load_excel(self.tableExel, path)

    def start_save_excel(self):
        path = self.path_excel_a if self.active_week == "A" else self.path_excel_b
        save_excel(self.tableExel, path, self.full_path)

    # ── Styles ─────────────────────────────────────────
    def set_styles(self):
        style_path = join(self.full_path, "desktop", "ui", "styles", "panel.css")
        try:
            with open(style_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print("Style file not found")

    # ── Events ─────────────────────────────────────────
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
