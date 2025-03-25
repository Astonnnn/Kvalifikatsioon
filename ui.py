#pyQt

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QAction, QMessageBox, QLineEdit, QPushButton
from PyQt5.QtGui import QIcon, QFont

from database import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kvalifikatsioon")
        self.setGeometry(0,0,500,500) #ekraani (algusX,algusY,laius, kõrgus), tuleks ära muuta, et suurus vastavalt monitorile ja ilmumine ekraani keskele
        #self.setWindowIcon(QIcon("")) #logo

        self.create_menu_bar()

        loo_andmebaas() #oleme kindlad, et andmebaas luuakse

        #sisestusväljad

        self.veebisaidi_nimi = QLabel("Sisesta veebisaidi URL:", self)
        self.veebisaidi_nimi.move(20,20)
        self.veebisaidi_sisend = QLineEdit(self)
        self.veebisaidi_sisend.setGeometry(150,20,300,30)

        self.ajalimiidi_nimi = QLabel("Sisesta ajalimiit (min):", self)
        self.ajalimiidi_nimi.move(20, 70)
        self.ajalimiidi_sisend = QLineEdit(self)
        self.ajalimiidi_sisend.setGeometry(150, 70, 100, 30)

        self.sisesta_nupp = QPushButton("Lisa veebileht", self)
        self.sisesta_nupp.setGeometry(150,120,150,40)
        self.sisesta_nupp.clicked.connect(self.salvesta_veebileht)


        self.näita_nupp = QPushButton("Näita olemasolevaid veebilehti", self)
        self.näita_nupp.setGeometry(150,170, 150, 40)
        self.näita_nupp.clicked.connect(kuva_veebilehed)

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

    def salvesta_veebileht(self):
        veebileht = self.veebisaidi_sisend.text().strip()
        ajalimiit = self.ajalimiidi_sisend.text().strip()

        #Kontroll et saadakse andmed kätte
        print(f"Veebileht: {veebileht}, Ajalimiit: {ajalimiit}")
        #TULEKS LISADA TINGIMUS MIS KONTROLLIB NENDE KEHTIVUST


        lisa_veebileht(veebileht, int(ajalimiit))
        print(f'{veebileht} lisatud valikusse ajalimiidiga {ajalimiit} minutit.')
        self.veebisaidi_sisend.clear()
        self.ajalimiidi_sisend.clear()




