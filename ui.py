#pyQt

import re

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QVBoxLayout, QAction, QMessageBox, \
    QPushButton, QTabWidget, QGridLayout, \
    QScrollArea, QHBoxLayout
from PyQt5.QtGui import QIcon

from components import ModernLabel, ModernLineEdit, ModernNumberInput, ModernButton, main_window_style, menu_bar_style
from database import *




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Veebisaidi blokeerija")
        self.setWindowIcon(QIcon(r'logod/peaaknaLogo.png'))
        self.setGeometry(100, 100, 1000, 900) #ekraani (algusX,algusY,laius, kõrgus), tuleks ära muuta, et suurus vastavalt monitorile ja ilmumine ekraani keskele
        self.setMinimumSize(900, 900)
        self.setStyleSheet(main_window_style())

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        create_database()  # oleme kindlad, et andmebaas luuakse

        self.frontpage()
        self.websites()
        self.tab_widget.setCurrentWidget(self.tab_frontpage)


        self.create_menu_bar()


    def frontpage(self):
        self.tab_frontpage = QWidget()

        self.tab_frontpage.setStyleSheet("""
            QWidget {
                background: white;
                border-radius: 20px; 
                margin: 10px
            }
        """)


        main_layout = QVBoxLayout()
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(40, 40, 40, 40)

        #Tiitel

        title_layout = QVBoxLayout()
        title_layout.setAlignment(Qt.AlignCenter)

        title = ModernLabel("Lisa uus veebileht", "title")
        title.setAlignment(Qt.AlignCenter)
        subtitle = ModernLabel("Määra ajalimiite veebilehtedele ning vähenda ekraaniaega", "normal")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #718096; font-size: 16px; margin-bottom: 20px;")

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        main_layout.addLayout(title_layout)


        #Sisestusväljad
        form_widget = QWidget()

        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(20)

        #URL/veebilehe sisestus

        url_layout = QVBoxLayout()
        url_label = ModernLabel("Sisesta veebisaidi URL:", "header")
        self.website_input = ModernLineEdit("nt. youtube.com")
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.website_input)

        #Ajalimiidi sisestus

        time_layout = QVBoxLayout()
        time_label = ModernLabel("Sisesta ajalimiit (min):", "header")
        self.time_input = ModernNumberInput("nt. 30", min_value=1, max_value=120)
        time_layout.addWidget(time_label)
        time_layout.addWidget(self.time_input)

        form_layout.addLayout(url_layout)
        form_layout.addLayout(time_layout)

        #Sisestusnupp

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.confirm_button = ModernButton("Lisa veebileht", "normal")
        self.confirm_button.clicked.connect(self.save_website)
        self.confirm_button.setMinimumWidth(150)
        button_layout.addWidget(self.confirm_button)
        button_layout.addStretch()

        form_layout.addLayout(button_layout)
        main_layout.addWidget(form_widget)

        #Lisame kõik alamjaotused main_layouti

        self.tab_frontpage.setLayout(main_layout)
        self.tab_widget.addTab(self.tab_frontpage, "Esileht")


    def websites(self):

        self.tab_websites = QWidget()
        layout = QVBoxLayout(self.tab_websites)


        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        layout.addWidget(scrollArea)

        scroll_content = QWidget()
        grid_layout = QGridLayout(scroll_content)

        titles = ['Nr', 'Veebileht', 'Ajalimiit', 'Staatus', 'Aega jäänud', 'Kustuta']

        for idx, text in enumerate(titles): #Võtab indeksi ja pealkirja
            label = QLabel(text)
            label.setStyleSheet('font-weight: bold; font-size: 16px') # Seab pealkirja paksuks ja suuremaks
            grid_layout.addWidget(label, 0, idx) # paneb pealkirja õigesse kohta

        data = show_websites()
        for a, i in enumerate(data, start = 1): #Võtab andme indeksiga
            lineNr, website, time_limit, status, remaining_time, question_showing = i #lahutab andmed üksteisest
            grid_layout.addWidget(QLabel(str(a)), a, 0)
            grid_layout.addWidget(QLabel(website), a, 1)
            grid_layout.addWidget(QLabel(str(time_limit)),a, 2)

            status_label = QLabel('Blokeerimata' if status ==0 else 'Blokeeritud')
            status_label.setStyleSheet('color: green' if status == 0 else 'color: red')
            grid_layout.addWidget(status_label, a, 3)
            grid_layout.addWidget(QLabel(str(remaining_time)), a, 4)
            delete_button = ModernButton('❌', "delete")
            delete_button.clicked.connect(lambda _, x=website: self.delete_and_refresh(x))
            grid_layout.addWidget(delete_button, a, 5)

        scrollArea.setWidget(scroll_content)
        scrollArea.verticalScrollBar()

        self.tab_websites.setLayout(layout)
        self.tab_widget.addTab(self.tab_websites, "Veebilehed")



    def create_menu_bar(self):
        #LOOME MENÜÜ
        menu_bar = self.menuBar() #loob menüübari, sinna saab lisada veel dropdowne
        menu_bar.setStyleSheet(menu_bar_style())

        file_menu = menu_bar.addMenu("Menüü 🏠") #lisab menüübaari menüü

        #LOOME JUHTUMISED
        help_action = QAction("Abi ❓", self)
        exit_action = QAction("Lahku 🚪", self)


        #ühendame sündmused liikmetega

        help_action.triggered.connect(self.help_menu)
        exit_action.triggered.connect(self.close_app)

        #LISAME JUHTUMISED MENÜÜSSE

        file_menu.addAction(help_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)


    # loome sündmused menüü liikmete jaoks
    def help_menu(self):
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

    def close_app(self):
        print("Väljumine võtab aset")
        self.close()

    def save_website(self):
        website = self.website_input.text().strip()
        time_limit = self.time_input.text().strip()



        if re.match(r'^[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$', website):
            #Kontroll et saadakse andmed kätte
            print(f"Veebileht: {website}, Ajalimiit: {time_limit}")

            add_website_and_time(website, int(time_limit))
            self.website_input.clear()
            self.time_input.clear()
            self.refresh_table()
        else:
            QMessageBox.warning(self, "Error", "Sisesta website korrektses formaadis!")

    def refresh_table(self):
        print(self.tab_widget)
        self.tab_widget.removeTab(self.tab_widget.indexOf(self.tab_websites))
        self.websites()

    def delete_and_refresh(self, website):
        delete_website(website)
        print("Veebileht kustutatud!")
        self.refresh_table()




