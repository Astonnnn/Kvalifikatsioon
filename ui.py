#pyQt

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QAction, QMessageBox, QLineEdit, \
    QPushButton, QDialog, QTabWidget, QFormLayout, QGridLayout
from PyQt5.QtGui import QIcon, QFont
from PyQt6.QtWidgets import QStackedWidget

from database import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kvalifikatsioon")
        self.setGeometry(0,0,500,500) #ekraani (algusX,algusY,laius, kõrgus), tuleks ära muuta, et suurus vastavalt monitorile ja ilmumine ekraani keskele
        #self.setWindowIcon(QIcon("")) #logo
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.esileht()
        self.veebilehed()
        self.tab_widget.setCurrentWidget(self.tab_esileht)

        loo_andmebaas()  # oleme kindlad, et andmebaas luuakse
        self.create_menu_bar()

    def esileht(self):
        self.tab_esileht = QWidget()

        mainLayout = QVBoxLayout()
        sisestusväljaLayout = QFormLayout()

        self.veebisaidi_nimi = QLabel("Sisesta veebisaidi URL:", self)
        self.veebisaidi_sisend = QLineEdit(self)
        sisestusväljaLayout.addRow(self.veebisaidi_nimi, self.veebisaidi_sisend)

        self.ajalimiidi_nimi = QLabel("Sisesta ajalimiit (min):", self)
        self.ajalimiidi_sisend = QLineEdit(self)
        sisestusväljaLayout.addRow(self.ajalimiidi_nimi, self.ajalimiidi_sisend)

        mainLayout.addLayout(sisestusväljaLayout)

        self.sisesta_nupp = QPushButton("Lisa veebileht", self)
        self.sisesta_nupp.clicked.connect(self.salvesta_veebileht)
        mainLayout.addLayout(sisestusväljaLayout)

        self.näita_nupp = QPushButton("Näita olemasolevaid veebilehti", self)
        self.näita_nupp.clicked.connect(kuva_veebilehed)

        mainLayout.addWidget(self.sisesta_nupp)
        mainLayout.addWidget(self.näita_nupp)

        #sätime layouti tabile ja lisame selle QTabWidgetisse

        self.tab_esileht.setLayout(mainLayout)
        self.tab_widget.addTab(self.tab_esileht, "Esileht")

    def veebilehed(self):
        self.tab_veebilehed = QWidget()
        layout = QGridLayout()

        andmed = kuva_veebilehed()
        pealkiri1 = QLabel("Veebileht")
        pealkiri1.setFont(QFont("Arial", 14, QFont.Bold))
        pealkiri2 = QLabel("Ajalimiit")
        pealkiri2.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(pealkiri1, 0, 1)
        layout.addWidget(pealkiri2, 0, 2)


        for i in range(0, len(andmed)):
            layout.addWidget(QLabel(str(andmed[i][0])), i+1, 0)
            layout.addWidget(QLabel(str(andmed[i][1])), i+1, 1)
            layout.addWidget(QLabel(str(andmed[i][2])), i+1, 2)

        self.tab_veebilehed.setLayout(layout)
        self.tab_widget.addTab(self.tab_veebilehed, "Veebilehed")


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




