from PyQt5.QtWidgets import (
    QApplication, QDialog, QLabel, QVBoxLayout, QRadioButton,
    QButtonGroup, QPushButton, QMessageBox
)
from question_manager import generate_mcq


class QuestionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Küsimus")
        self.setModal(True)
        self.setGeometry(100, 100, 300, 200)
        self.result = None

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        try:
            vastus = generate_mcq("science").split(";")
            if len(vastus) < 6:
                raise ValueError("Invalid question format")

            küsimus, valik1, valik2, valik3, valik4 = vastus[:5]
            self.oigeVastus = vastus[5].strip()

            # Fix correct answer formatting
            for i in self.oigeVastus[::-1]:
                if i.isupper() and i in ['A', 'B', 'C', 'D']:
                    self.oigeVastus = i
                    break

            layout.addWidget(QLabel(küsimus))

            self.button_group = QButtonGroup(self)
            self.rb = []

            for i, valik in enumerate([valik1, valik2, valik3, valik4]):
                rb = QRadioButton(valik)
                self.button_group.addButton(rb, i)
                layout.addWidget(rb)
                self.rb.append(rb)

            self.vasta_button = QPushButton("Vasta")
            self.vasta_button.clicked.connect(self.kontrolli_vastust)
            layout.addWidget(self.vasta_button)

        except Exception as e:
            print(f"Error generating question: {e}")
            layout.addWidget(QLabel("Viga küsimuse genereerimisel"))
            self.result = False

        self.setLayout(layout)

    def kontrolli_vastust(self):
        if not hasattr(self, 'button_group'):
            self.reject()
            return

        id = self.button_group.checkedId()
        if id == -1:
            QMessageBox.warning(self, 'Hoiatus', 'Palun vali vastus enne vastamist.')
            return

        valikud = ['A', 'B', 'C', 'D']
        oige_index = valikud.index(self.oigeVastus)

        if id == oige_index:
            QMessageBox.information(self, 'Tulemus', 'Õige vastus!')
            self.result = True
            self.accept()
        else:
            QMessageBox.information(self, 'Tulemus', f'Vale vastus! Õige oli: {self.oigeVastus}')
            self.result = False
            self.accept()


def run_app(parent=None):
    try:
        dialog = QuestionDialog(parent)
        dialog.exec_()
        return dialog.result
    except Exception as e:
        print(f"Error in run_app: {e}")
        return False

if __name__ == '__main__':
    run_app()
