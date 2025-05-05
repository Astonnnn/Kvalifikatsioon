#peaprogramm

import sys
from PyQt5.QtWidgets import QApplication
from ui import MainWindow
import os
from kusimused import Popup
def main():
    app = QApplication(sys.argv) #käivitab programmi
    window = MainWindow()#kutsub ui.py klassi välja
    window.resize(500, 400)
    window.show() #näitab akent
    sys.exit(app.exec_()) #hoiab akna avatuna kuniks ristile vajutatakse
if __name__ == "__main__":
    main()
