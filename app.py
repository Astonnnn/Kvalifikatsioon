import sys
from PyQt5.QtWidgets import QApplication
from ui import MainWindow
import api_server
import threading
from question_area import run_app
from database import change_status, restore_time, change_question_show_status


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(300, 300)

    api_server.set_main_window(window)

    def handle_dialog(domain):
        change_question_show_status(domain)
        result = run_app(window)
        change_question_show_status(domain)
        print(result)
        if result:
            change_status(domain)
            restore_time(domain)
        else:
            restore_time(domain)

    api_server.signals.show_dialog.connect(handle_dialog)

    flask_thread = threading.Thread(target=api_server.run_flask, daemon=True)
    flask_thread.start()

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
