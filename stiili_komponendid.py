#Disain, töötab samamoodi nagu tavaline css || dokum. -> https://doc.qt.io/qtforpython-6/tutorials/basictutorial/widgetstyling.html

from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QMainWindow
from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtCore import Qt


def peaakna_disain():
    return """
        QMainWindow {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                            stop:0 #f7fafc, stop:1 #edf2f7);
        }
        QTabWidget::pane {
            border: none;
            background: transparent;
        }
        QTabBar::tab {
            background: rgba(255, 255, 255, 0.7);
            color: #4a5568;
            padding: 12px 24px;
            margin: 2px;
            border-radius: 12px 12px 0 0;
            font-weight: 600;
            font-size: 14px;
            min-width: 120px;
            margin-left: 10px
        }
        QTabBar::tab:selected {
                background: white;
                color: #667eea;
            }
        QTabBar::tab:hover:!selected {
            background-color: white;
            color: #8a9ceb;
            }
    """

def menüü_bari_kujundus():
    return """
        QMenuBar {
            background: white;
            color: #2d3748;
            border-bottom: 1px solid rgba(102, 126, 234, 0.1);
            padding: 5px;
            font-size: 14px;
        }
        QMenuBar::item {
                background: transparent;
                padding: 8px 16px;
                border-radius: 8px;
                margin: 0 4px;
            }
        QMenuBar::item:selected {
                background: rgba(102, 126, 234, 0.1);
                color: #667eea;
            }
         QMenu {
                background: white;
                border: 1px solid rgba(102, 126, 234, 0.2);
                border-radius: 12px;
                padding: 8px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            }
            QMenu::item {
                padding: 8px 16px;
                border-radius: 8px;
                margin: 2px;
            }
            QMenu::item:selected {
                background: rgba(102, 126, 234, 0.1);
                color: #667eea;
            }
        """



class disainiga_nupp(QPushButton):
    def __init__(self, text, nupu_liik="normal"):
        super().__init__(text)
        self.nupu_liik = nupu_liik
        self.setFont(QFont("Segoe UI", 10, QFont.Medium))
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(45)
        self.stiilid()


    def stiilid(self):
        if self.nupu_liik == "normal":
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #667eea, stop:1 #764ba2);
                    color: white;
                    border: none;
                    border-radius: 12px;
                    padding: 12px 24px;
                    font-weight: 600;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #5a6fd8, stop:1 #6a4190);
                    transform: translateY(-2px);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #4c5bc6, stop:1 #5e3a7e);
                }
            """)
        elif self.nupu_liik == "delete":
            self.setStyleSheet("""
                            QPushButton {
                                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #ff6b6b, stop:1 #ee5a52);
                                color: white;
                                border: none;
                                border-radius: 8px;
                                padding: 8px 12px;
                                font-weight: 600;
                                font-size: 12px;
                                min-width: 40px;
                                max-width: 40px;
                                min-height: 35px;
                                max-height: 35px;
                            }
                            QPushButton:hover {
                                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #ff5252, stop:1 #e53e3e);
                            }
                            QPushButton:pressed {
                                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #e53e3e, stop:1 #c53030);
                            }
                            """)

class disainiga_sisestusväli(QLineEdit):
    def __init__(self, kohahoidja=""):
        super().__init__()
        self.setPlaceholderText(kohahoidja)
        self.setFont(QFont("Segoe UI", 11))
        self.setMinimumHeight(45)
        self.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.9);
                border: 2px solid rgba(102, 126, 234, 0.3);
                border-radius: 12px;
                padding: 12px 16px;
                font-size: 14px;
                color: #2d3748;
            }
            QLineEdit:focus {
                border: 2px solid #667eea;
                background-color: white;
                outline: none;
            }
        """)


class disainiga_sisestusväli_number(disainiga_sisestusväli):
    def __init__(self, kohahoidja="", vähim_väärtus=1, suurim_väärtus=9999):
        super().__init__(kohahoidja)
        validator = QIntValidator(vähim_väärtus, suurim_väärtus)
        self.setValidator(validator)


class disainiga_tekst(QLabel):
    def __init__(self, text, teksti_liik="normal"):
        super().__init__(text)
        self.teksti_liik = teksti_liik
        self.stiilid()

    def stiilid(self):
        if self.teksti_liik == "title":
            self.setFont(QFont("Segoe UI", 24, QFont.Bold))
            self.setStyleSheet("""
                QLabel {
                    color: #2d3748;
                    margin-bottom: 10px;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #667eea, stop:1 #764ba2);
                    -webkit-background-clip: text;
                    background-clip: text;
                }
            """)
        elif self.teksti_liik == "header":
            self.setFont(QFont("Segoe UI", 16, QFont.DemiBold))
            self.setStyleSheet("""
                QLabel {
                    color: #4a5568;
                    margin-bottom: 8px;
                    padding: 8px 0;
                }
            """)
        elif self.teksti_liik == "table_header":
            self.setFont(QFont("Segoe UI", 12, QFont.Bold))
            self.setStyleSheet("""
                QLabel {
                    color: #2d3748;
                    padding: 12px 8px;
                    background-color: rgba(102, 126, 234, 0.1);
                    border-radius: 8px;
                }
            """)
        else:  # tavaline
            self.setFont(QFont("Segoe UI", 11))
            self.setStyleSheet("""
                QLabel {
                    color: #4a5568;
                    padding: 4px 8px;
                }
            """)
