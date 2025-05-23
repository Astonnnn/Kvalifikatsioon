import sys
from PyQt5.QtWidgets import QApplication
from ui import MainWindow
import api_server
import threading
from küsimuse_kast import run_app
from andmebaas import muuda_staatus, taasta_aeg, muuda_küsimise_kuvamise_staatus


def main():
    #peaaken
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(300, 300)

    api_server.set_main_window(window)

    #kuvab küsimuse ning vastavalt vastusele käitub edasi
    def handle_dialog(veebileht):
        muuda_küsimise_kuvamise_staatus(veebileht)
        tulemus = run_app(window)
        muuda_küsimise_kuvamise_staatus(veebileht)
        print(tulemus)
        if tulemus:
            muuda_staatus(veebileht)
            taasta_aeg(veebileht)
        else:
            taasta_aeg(veebileht)

    api_server.signals.show_dialog.connect(handle_dialog)

    flask_thread = threading.Thread(target=api_server.run_flask, daemon=True)
    flask_thread.start()

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
