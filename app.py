#peaprogramm

import sys
from PyQt5.QtWidgets import QApplication
from ui import MainWindow

def main():
    app = QApplication(sys.argv) #käivitab programmi
    window = MainWindow() #kutsub ui.py klassi välja
    window.show() #näitab akent
    sys.exit(app.exec_()) #hoiab akna avatuna kuniks ristile vajutatakse

if __name__ == "__main__":
    main()