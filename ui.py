#pyQt

import re

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QVBoxLayout, QAction, QMessageBox, \
    QPushButton, QTabWidget, QGridLayout, \
    QScrollArea, QHBoxLayout
from PyQt5.QtGui import QIcon

from stiili_komponendid import disainiga_tekst, disainiga_sisestusväli, disainiga_sisestusväli_number, disainiga_nupp, peaakna_disain, menüü_bari_kujundus
from andmebaas import *




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Veebisaidi blokeerija")
        self.setWindowIcon(QIcon(r'logod/peaaknaLogo.png'))
        self.setGeometry(100, 100, 1000, 900) #ekraani (algusX,algusY,laius, kõrgus), tuleks ära muuta, et suurus vastavalt monitorile ja ilmumine ekraani keskele
        self.setMinimumSize(900, 900)
        self.setStyleSheet(peaakna_disain())

        self.tab_vidin = QTabWidget()
        self.setCentralWidget(self.tab_vidin)

        loo_andmebaas()  # oleme kindlad, et andmebaas luuakse

        self.esileht()
        self.veebilehed()
        self.tab_vidin.setCurrentWidget(self.tab_esileht)


        self.create_menu_bar()


    def esileht(self):
        self.tab_esileht = QWidget()

        self.tab_esileht.setStyleSheet("""
            QWidget {
                background: white;
                border-radius: 20px; 
                margin: 10px
            }
        """)


        peamine_paigutus = QVBoxLayout()
        peamine_paigutus.setSpacing(30)
        peamine_paigutus.setContentsMargins(40, 40, 40, 40)

        #Tiitel

        tiitli_paigutus = QVBoxLayout()
        tiitli_paigutus.setAlignment(Qt.AlignCenter)

        tiitel = disainiga_tekst("Lisa uus veebileht", "title")
        tiitel.setAlignment(Qt.AlignCenter)
        alamtiitel = disainiga_tekst("Määra ajalimiite veebilehtedele ning vähenda ekraaniaega", "normal")
        alamtiitel.setAlignment(Qt.AlignCenter)
        alamtiitel.setStyleSheet("color: #718096; font-size: 16px; margin-bottom: 20px;")

        tiitli_paigutus.addWidget(tiitel)
        tiitli_paigutus.addWidget(alamtiitel)
        peamine_paigutus.addLayout(tiitli_paigutus)


        #Sisestusväljad
        sisestusvälja_vidin = QWidget()

        sisestusvälja_paigutus= QVBoxLayout(sisestusvälja_vidin)
        sisestusvälja_paigutus.setSpacing(20)

        #URL/veebilehe sisestus

        url_paigutus = QVBoxLayout()
        url_pealkiri = disainiga_tekst("Sisesta veebisaidi URL:", "header")
        self.url_sisestusväli= disainiga_sisestusväli("nt. youtube.com")
        url_paigutus.addWidget(url_pealkiri)
        url_paigutus.addWidget(self.url_sisestusväli)

        #Ajalimiidi sisestus

        aja_paigutus = QVBoxLayout()
        aja_pealkiri = disainiga_tekst("Sisesta ajalimiit (min):", "header")
        self.aja_sisestusväli= disainiga_sisestusväli_number("nt. 30", vähim_väärtus=1, suurim_väärtus=120)
        aja_paigutus.addWidget(aja_pealkiri)
        aja_paigutus.addWidget(self.aja_sisestusväli)

        sisestusvälja_paigutus.addLayout(url_paigutus)
        sisestusvälja_paigutus.addLayout(aja_paigutus)

        #Sisestusnupp

        sisestusnupu_paigutus = QHBoxLayout()
        sisestusnupu_paigutus.addStretch()
        self.sisestusnupp = disainiga_nupp("Lisa veebileht", "normal")
        self.sisestusnupp.clicked.connect(self.salvesta_veebileht)
        self.sisestusnupp.setMinimumWidth(150)
        sisestusnupu_paigutus.addWidget(self.sisestusnupp)
        sisestusnupu_paigutus.addStretch()

        sisestusvälja_paigutus.addLayout(sisestusnupu_paigutus)
        peamine_paigutus.addWidget(sisestusvälja_vidin)

        #Lisame kõik alamjaotused main_layouti

        self.tab_esileht.setLayout(peamine_paigutus)
        self.tab_vidin.addTab(self.tab_esileht, "➕ Esileht")


    def veebilehed(self):

        self.tab_veebilehed = QWidget()
        self.tab_veebilehed.setStyleSheet("""
            QWidget {
                background: white;
                border-radius: 20px;
                margin: 10px
            }
        """)

        paigutus = QVBoxLayout()
        paigutus.setContentsMargins(40, 40, 40, 40)
        paigutus.setSpacing(25)

        #Pealkiri

        pealkirja_paigutus = QVBoxLayout()
        pealkirja_paigutus.setAlignment(Qt.AlignCenter)

        pealkiri = disainiga_tekst("Hallatavad veebisaidid", "title")
        pealkiri.setAlignment(Qt.AlignCenter)
        pealkirja_paigutus.addWidget(pealkiri)
        paigutus.addLayout(pealkirja_paigutus)

        #Tulba pealkirjad

        tulba_tiitlid = ['#', 'Veebileht', 'Ajalimiit', 'Staatus', 'Aega jäänud', 'Kustuta']
        tulba_pealkirja_paigutus = QGridLayout()
        for idx, text in enumerate(tulba_tiitlid):  # Võtab indeksi ja pealkirja
            pealkiri = disainiga_tekst(text, "table_header")
            tulba_pealkirja_paigutus.addWidget(pealkiri, 0, idx)

        paigutus.addLayout(tulba_pealkirja_paigutus)

        kerimisala = QScrollArea()
        kerimisala.setWidgetResizable(True)
        paigutus.addWidget(kerimisala)

        kerimise_sisu = QWidget()
        tabeli_paigutus = QGridLayout()
        tabeli_paigutus.setAlignment(Qt.AlignTop)
        kerimise_sisu.setLayout(tabeli_paigutus)


         # paneb pealkirja õigesse kohta

        andmed = kuva_veebilehed()
        for a, i in enumerate(andmed, start = 1): #Võtab andme indeksiga
            järje_nr, veebileht, aja_limiit, staatus, jäänud_aeg, küsimus_kuvatud = i #lahutab andmed üksteisest
            tabeli_paigutus.addWidget(disainiga_tekst(str(a), "normal"), a, 0)
            tabeli_paigutus.addWidget(disainiga_tekst(veebileht, "normal"), a, 1)
            tabeli_paigutus.addWidget(disainiga_tekst(f'{str(aja_limiit)} min' , "normal"),a, 2)

            staatuse_olek = disainiga_tekst('Blokeerimata' if staatus ==0 else 'Blokeeritud', "normal")
            staatuse_olek.setStyleSheet('color: green' if staatus == 0 else 'color: red')
            tabeli_paigutus.addWidget(staatuse_olek, a, 3)
            tabeli_paigutus.addWidget(disainiga_tekst(f'{str(round(jäänud_aeg/60, 1))} min', "normal"), a, 4)
            kustuta_nupp = disainiga_nupp('❌', "delete")
            kustuta_nupp.clicked.connect(lambda _, x=veebileht: self.kustuta_ja_värskenda(x))
            tabeli_paigutus.addWidget(kustuta_nupp, a, 5)

        kerimisala.setWidget(kerimise_sisu)
        kerimisala.verticalScrollBar()


        self.värskenda_nupp = disainiga_nupp("Värskenda 🔄", "normal")
        self.värskenda_nupp.clicked.connect(lambda: (self.varskenda_tabel(), self.tab_vidin.setCurrentWidget(self.tab_veebilehed)))
        paigutus.addWidget(self.värskenda_nupp)

        self.tab_veebilehed.setLayout(paigutus)
        self.tab_vidin.addTab(self.tab_veebilehed, "🌐 Veebilehed")



    def create_menu_bar(self):
        #LOOME MENÜÜ
        menüü_loend = self.menuBar() #loob menüübari, sinna saab lisada veel dropdowne
        menüü_loend.setStyleSheet(menüü_bari_kujundus())

        faili_menüü = menüü_loend.addMenu("Menüü 🏠") #lisab menüübaari menüü

        #LOOME JUHTUMISED
        abi = QAction("Abi ❓", self)
        lahku = QAction("Lahku 🚪", self)


        #ühendame sündmused liikmetega

        abi.triggered.connect(self.abi_menyy)
        lahku.triggered.connect(self.sulge_rakendus)

        #LISAME JUHTUMISED MENÜÜSSE

        faili_menüü.addAction(abi)
        faili_menüü.addSeparator()
        faili_menüü.addAction(lahku)


    # loome sündmused menüü liikmete jaoks
    def abi_menyy(self):
        msg = QMessageBox()
        msg.setWindowTitle("Abi")
        msg.setText("""
            <h2>Kuidas rakendust kasutada?</h2>
            <p><b>1. Veebilehe lisamine:</b> Sisesta soovitud veebilehe URL ning aeg minutites</p>
            <p><b>2. Veebilehtede jälgimine:</b> Mine veebilehtede alalehele ning jälgi veebilehtede järelolevat aega ja staatust</p>
            <p><b>3. Aja haldamine:</b> Ajalimiidi lõppemisel tuleb vastata küsimusele, millele õigesti vastamisel ajalimiit taastatakse</p>
            <p><b>4. Veebilehe kustutamine:</b> Vajuta ❌ nupule, et eemaldada veebileht valikust</p>
            """)

        msg.setStyleSheet("""
                QMessageBox {
                    background: white;
                    border-radius: 12px;
                }
                QMessageBox QLabel {
                    color: #2d3748;
                    font-size: 14px;
                    padding: 10px;
                }
                """)
        msg.exec_()

    def sulge_rakendus(self):
        self.close()

    def salvesta_veebileht(self):
        veebileht = self.url_sisestusväli.text().strip()
        aja_limiit = self.aja_sisestusväli.text().strip()



        if re.match(r'^[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$', veebileht):
            #Kontroll et saadakse andmed kätte
            print(f"Veebileht: {veebileht}, Ajalimiit: {aja_limiit}")

            lisa_veebileht_ja_aeg(veebileht, int(aja_limiit))
            self.url_sisestusväli.clear()
            self.aja_sisestusväli.clear()
            self.varskenda_tabel()
        else:
            QMessageBox.warning(self, "Error", "Sisesta veebileht korrektses formaadis!")

    def varskenda_tabel(self):
        print(self.tab_vidin)
        self.tab_vidin.removeTab(self.tab_vidin.indexOf(self.tab_veebilehed))
        self.veebilehed()

    def kustuta_ja_värskenda(self, veebileht):
        kustuta_veebileht(veebileht)
        print("Veebileht kustutatud!")
        self.varskenda_tabel()
        self.kuva_veebilehtede_tabel()

    def kuva_veebilehtede_tabel(self):
        self.tab_vidin.setCurrentWidget(self.tab_veebilehed)




