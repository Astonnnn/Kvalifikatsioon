import sys
from PyQt5.QtWidgets import QApplication
from ui import MainWindow
import api_server
import threading
from kusimused import run_app
from database import muuda_staatust, taasta_aeg


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(300, 300)

    # Setup signals
    api_server.set_main_window(window)

    def handle_dialog(domeen):
        result = run_app(window)
        if result:
            muuda_staatust(domeen)
            taasta_aeg(domeen)

    api_server.signals.show_dialog.connect(handle_dialog)

    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=api_server.run_flask, daemon=True)
    flask_thread.start()

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
