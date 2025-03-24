#pyQt

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QAction, QMessageBox
from PyQt5.QtGui import QIcon, QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kvalifikatsioon")
        self.setGeometry(0,0,500,500) #ekraani (algusX,algusY,laius, kõrgus), tuleks ära muuta, et suurus vastavalt monitorile ja ilmumine ekraani keskele
        #self.setWindowIcon(QIcon("")) #logo

        self.create_menu_bar()


    def create_menu_bar(self):
        #LOOME MENÜÜ
        menu_bar = self.menuBar() #loob menüübari, sinna saab lisada veel dropdowne
        file_menu = menu_bar.addMenu("File") #lisab menüübaari menüü

        #LOOME JUHTUMISED
        help_action = QAction("Help", self)
        exit_action = QAction("Exit", self)




        #ühendame sündmused liikmetega

        help_action.triggered.connect(self.help_menu)
        exit_action.triggered.connect(self.close_app)

         #LISAME JUHTUMISED MENÜÜSSE

        file_menu.addAction(help_action)
        file_menu.addAction(exit_action)


    # loome sündmused menüü liikmete jaoks
    def help_menu(self):
        print("Abi on saabumas!")

    def close_app(self):
        print("Väljumine võtab aset")
        self.close()





