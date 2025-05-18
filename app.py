#peaprogramm

import sys
from PyQt5.QtWidgets import QApplication
from ui import MainWindow
import os
from kusimused import Popup
from api_server import *
import threading


def main():
    app = QApplication(sys.argv)  # käivitab programmi
    window = MainWindow()#kutsub ui.py klassi välja
    window.resize(700, 800)
    window.show() #näitab akent
    set_main_window_reference(window)

    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    sys.exit(app.exec_()) #hoiab akna avatuna kuniks ristile vajutatakse
if __name__ == "__main__":
    main()
