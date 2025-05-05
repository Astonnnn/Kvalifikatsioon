#See veits eraldi koodist aga pmst võtab staatuse ja siis vastavalt kerib ühe kohta aega

import time
from database import kuva_veebilehed
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMainWindow, QLabel, QDialog, QRadioButton, QButtonGroup, \
    QPushButton, QMessageBox, QApplication
from question_manager import *
from PyQt5.QtCore import QTimer


class Popup(QWidget):
    def __init__(self, main_window):
        super().__init__()
        #self.setWindowTitle('Küsimus')
        #self.main_window = main_window


        layout = QVBoxLayout()
        self.setLayout(layout)

        QTimer.singleShot(0, self.aja_vaatamine)

    def aja_vaatamine(self):
        print("aja_vaatamine started")
        koik_veebilehed = kuva_veebilehed()
        print(koik_veebilehed)

        blokeeritud = []
        for i in koik_veebilehed: #Otsib veebilehe mis prg tööl e blokeeritud lehe
            if i[3] == 1:
                blokeeritud.append(i)

        if blokeeritud:
            blokeeritud = blokeeritud[0]
            print(blokeeritud)

            maksimaalneaeg = blokeeritud[3] * 3

            algne = time.time()
            praegune = algne
            while praegune - algne < maksimaalneaeg: # Kontrollib et millal paneb küsimuse ette
                praegune = time.time()
            self.genereeri_kysimus()

    def genereeri_kysimus(self):
        vastus = generate_mcq("science").split(";")
        küsimus = vastus[0]
        valik1 = vastus[1]
        valik2 = vastus[2]
        valik3 = vastus[3]
        valik4 = vastus[4]
        self.oigeVastus = vastus[5].strip(' \n\n')

        # Determine the correct answer
        for i in self.oigeVastus[::-1]:
            if i.isupper() and i in ['A', 'B', 'C', 'D']:
                self.oigeVastus = i
                break

        dialog = QDialog(self)
        dialog.setWindowTitle("Küsimus")
        dialog.setGeometry(100, 100, 300, 150)

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
            valitud_nupp = button_group.button(valitud_id)

            valikud = ['A', 'B', 'C', 'D']
            oigeVastus2 = valikud.index(self.oigeVastus)

            if valitud_nupp:
                if valitud_id == (oigeVastus2 + 1):
                    QMessageBox.information(dialog, 'Tulemus', 'Õige vastus!')
                else:
                    QMessageBox.information(dialog, 'Tulemus', f'Vale vastus! Õige oli: {self.oigeVastus}')
                dialog.accept()
            else:
                QMessageBox.warning(dialog, 'Hoiatus', 'Palun vali vastus enne vastamist.')

        vasta.clicked.connect(kontrolli_vastust)

        dialog.setLayout(layout)
        dialog.exec_()



if __name__ == "__main__":
    app = QApplication([])

    popup = Popup(None)

    app.exec_()
