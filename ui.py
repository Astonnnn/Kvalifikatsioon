#pyQt

import sys
import re

from PyQt5.QtCore import QRegExp
from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QVBoxLayout, QAction, QMessageBox, QLineEdit, \
    QPushButton, QTabWidget, QFormLayout, QGridLayout, QDialog, QRadioButton, QButtonGroup
from PyQt5.QtGui import QIcon, QFont, QIntValidator, QRegExpValidator



import question_manager
from question_manager import generate_mcq

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
        self.seaded()
        self.küsimused()
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
        layout = QGridLayout()

        andmed = kuva_veebilehed()
        pealkiri1 = QLabel("Nr")
        pealkiri1.setFont(QFont("Arial", 14, QFont.Bold))
        pealkiri2 = QLabel("Veebileht")
        pealkiri2.setFont(QFont("Arial", 14, QFont.Bold))
        pealkiri3 = QLabel("Ajalimiit")
        pealkiri3.setFont(QFont("Arial", 14, QFont.Bold))
        pealkiri4 = QLabel("Staatus")
        pealkiri4.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(pealkiri1, 0, 0)
        layout.addWidget(pealkiri2, 0, 1)
        layout.addWidget(pealkiri3, 0, 2)
        layout.addWidget(pealkiri4, 0, 3)


        #kuvame veebilehtede andmed aknale
        for i in range(0, len(andmed)):
            layout.addWidget(QLabel(str(andmed[i][0])), i+1, 0)
            layout.addWidget(QLabel(str(andmed[i][1])), i+1, 1)
            layout.addWidget(QLabel(str(andmed[i][2])), i+1, 2)
            if andmed[i][3] == 0:
                staatus_kiri = QLabel('Blokeerimata')
                staatus_kiri.setStyleSheet("color: green")
                layout.addWidget(staatus_kiri, i+1, 3)
            else:
                staatus_kiri = QLabel('Blokeeritud')
                staatus_kiri.setStyleSheet("color: red")
                layout.addWidget(staatus_kiri, i+1, 3)

        self.tab_veebilehed.setLayout(layout)
        self.tab_widget.addTab(self.tab_veebilehed, "Veebilehed")

    def seaded(self):
        self.tab_seaded = QWidget()
        layout = QFormLayout()

        self.vanus = QLineEdit(self)
        self.vanus.setValidator(QIntValidator())
        layout.addRow("Vanus (aastates): ", self.vanus)


        self.tab_seaded.setLayout(layout)
        self.tab_widget.addTab(self.tab_seaded, "Seaded")


    def küsimused(self):
        self.tab_küsimused = QWidget()
        layout = QVBoxLayout()

        self.genereeri = QPushButton("Genereeri", self)
        self.genereeri.clicked.connect(self.genereeri_kysimus)

        layout.addWidget(self.genereeri)
        self.tab_küsimused.setLayout(layout)
        self.tab_widget.addTab(self.tab_küsimused, "Küsimused")



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
            #TULEKS LISADA TINGIMUS MIS KONTROLLIB, KAS VEEBILEHT ON JUBA LISATUD NING VASTAVALT SIIS MUUTA AEG, MITTE LISADA


            lisa_veebileht(veebileht, int(ajalimiit))
            print(f'{veebileht} lisatud valikusse ajalimiidiga {ajalimiit} minutit.')
            self.veebisaidi_sisend.clear()
            self.ajalimiidi_sisend.clear()
            self.varskenda_veebileht()
        else:
            QMessageBox.warning(self, "Error", "Sisesta veebileht korrektses formaadis!")

    def genereeri_kysimus(self):
        vastus = generate_mcq("science").split(";")
        print(vastus)
        küsimus = vastus[0]
        valik1 = vastus[1]
        valik2 = vastus[2]
        valik3 = vastus[3]
        valik4 = vastus[4]
        self.oigeVastus = vastus[5].strip(' \n\n')
        for i in self.oigeVastus[::-1]:
            if i.isupper() == True and i in ['A','B','C','D']:
                self.oigeVastus = i
                break

        dialog = QDialog(self)
        dialog.setWindowTitle("Küsimus")
        dialog.setGeometry(100,100,300,150)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(küsimus))

        rb1 = QRadioButton(valik1)
        rb2 = QRadioButton(valik2)
        rb3 = QRadioButton(valik3)
        rb4 = QRadioButton(valik4)

        button_group = QButtonGroup(dialog)
        button_group.addButton(rb1, 1)
        button_group.addButton(rb2, 2)
        button_group.addButton(rb3, 3)
        button_group.addButton(rb4, 4)

        layout.addWidget(rb1)
        layout.addWidget(rb2)
        layout.addWidget(rb3)
        layout.addWidget(rb4)

        vasta = QPushButton('Vasta')
        layout.addWidget(vasta)


        def kontrolli_vastust():
            valitud_id = button_group.checkedId()
            print(valitud_id)
            valitud_nupp = button_group.button(valitud_id)

            valikud = ['A','B','C','D']
            oigeVastus2 = valikud.index(self.oigeVastus)


            if valitud_nupp:
                #valitud_tekst = valitud_nupp.text()
                if valitud_id == (oigeVastus2+1):
                    QMessageBox.information(dialog, 'Tulemus', 'Õige vastus!')
                else:
                    QMessageBox.information(dialog, 'Tulemus', f'Vale vastus! Õige oli: {self.oigeVastus}')
                dialog.accept()
            else:
                QMessageBox.warning(dialog, 'Hoiatus', 'Palun vali vastus enne vastamist.')

        vasta.clicked.connect(kontrolli_vastust)

        dialog.setLayout(layout)
        dialog.exec_()

    def varskenda_veebileht(self):
        print(self.tab_widget)
        self.tab_widget.removeTab(self.tab_widget.indexOf(self.tab_veebilehed))
        self.veebilehed()






