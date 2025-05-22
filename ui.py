#pyQt

import re
from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QVBoxLayout, QAction, QMessageBox, QLineEdit, \
    QPushButton, QTabWidget, QFormLayout, QGridLayout,\
    QScrollArea
from PyQt5.QtGui import QIntValidator

from database import *




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kvalifikatsioon")
        self.setGeometry(0,0,500,500) #ekraani (algusX,algusY,laius, kõrgus), tuleks ära muuta, et suurus vastavalt monitorile ja ilmumine ekraani keskele
        #self.setWindowIcon(QIcon("")) #logo
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        loo_andmebaas()  # oleme kindlad, et andmebaas luuakse

        self.esileht()
        self.veebilehed()
        self.tab_widget.setCurrentWidget(self.tab_esileht)


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
        self.ajalimiidi_sisend.setValidator(QIntValidator())
        sisestusväljaLayout.addRow(self.ajalimiidi_nimi, self.ajalimiidi_sisend)

        mainLayout.addLayout(sisestusväljaLayout)

        self.sisesta_nupp = QPushButton("Lisa veebileht", self)
        self.sisesta_nupp.clicked.connect(self.salvesta_veebileht)
        mainLayout.addLayout(sisestusväljaLayout)


        mainLayout.addWidget(self.sisesta_nupp)

        #sätime layouti tabile ja lisame selle QTabWidgetisse

        self.tab_esileht.setLayout(mainLayout)
        self.tab_widget.addTab(self.tab_esileht, "Esileht")


    def veebilehed(self):

        self.tab_veebilehed = QWidget()
        layout = QVBoxLayout(self.tab_veebilehed)


        kerimine = QScrollArea()
        kerimine.setWidgetResizable(True)
        layout.addWidget(kerimine)

        scroll_content = QWidget()
        grid_layout = QGridLayout(scroll_content)

        pealkirjad = ['Nr', 'Veebileht', 'Ajalimiit', 'Staatus', 'Aega jäänud', 'Kustuta']

        for idx, text in enumerate(pealkirjad): #Võtab indeksi ja pealkirja
            label = QLabel(text)
            label.setStyleSheet('font-weight: bold; font-size: 16px') # Seab pealkirja paksuks ja suuremaks
            grid_layout.addWidget(label, 0, idx) # paneb pealkirja õigesse kohta

        andmed = kuva_veebilehed()
        for a, i in enumerate(andmed, start = 1): #Võtab andme indeksiga
            jarjenr, veebileht, ajalimiit, staatus, jaanud_aega, kysimus_ees = i #lahutab andmed üksteisest
            grid_layout.addWidget(QLabel(str(a)), a, 0)
            grid_layout.addWidget(QLabel(veebileht), a, 1)
            grid_layout.addWidget(QLabel(str(ajalimiit)),a, 2)

            staatus_kiri = QLabel('Blokeerimata' if staatus ==0 else 'Blokeeritud')
            staatus_kiri.setStyleSheet('color: green' if staatus == 0 else 'color: red')
            grid_layout.addWidget(staatus_kiri, a, 3)
            grid_layout.addWidget(QLabel(str(jaanud_aega)), a, 4)
            kustuta_nupp = QPushButton('❌', self)
            kustuta_nupp.clicked.connect(lambda _, x=veebileht: self.kustuta_ja_varskenda(x))
            grid_layout.addWidget(kustuta_nupp, a, 5)

        kerimine.setWidget(scroll_content)
        kerimine.verticalScrollBar()

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



        if re.match(r'^[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$', veebileht):
            #Kontroll et saadakse andmed kätte
            print(f"Veebileht: {veebileht}, Ajalimiit: {ajalimiit}")

            lisa_veebileht(veebileht, int(ajalimiit))
            print(f'{veebileht} lisatud valikusse ajalimiidiga {ajalimiit} minutit.')
            self.veebisaidi_sisend.clear()
            self.ajalimiidi_sisend.clear()
            self.varskenda_tabel()
        else:
            QMessageBox.warning(self, "Error", "Sisesta veebileht korrektses formaadis!")

    def varskenda_tabel(self):
        print(self.tab_widget)
        self.tab_widget.removeTab(self.tab_widget.indexOf(self.tab_veebilehed))
        self.veebilehed()

    def kustuta_ja_varskenda(self, veebileht):
        kustuta_veebileht(veebileht)
        print("Veebileht kustutatud!")
        self.varskenda_tabel()




