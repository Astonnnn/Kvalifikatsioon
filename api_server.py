from flask import Flask, request, jsonify
from flask_cors import CORS
from database import *
from urllib.parse import urlparse
import threading
from PyQt5.QtCore import QObject, pyqtSignal

app = Flask(__name__)
CORS(app)

class DialogSignals(QObject):
    show_dialog = pyqtSignal(str)

signals = None

def set_main_window(window):
    global signals
    signals = DialogSignals(window)

def koosta_kysimus(domeen):
    signals.show_dialog.emit(domeen)


@app.route('/tabs', methods=['POST', 'GET'])
def receive_tabs():
    aeg_maha = kuva_veebilehed()
    if request.method == 'POST':
        data = request.get_json()
        url = data.get("urls", [])
        print(f'Avatud aken: {url[0]}')
        koik_lehed = []
        muudetud_ajad = []
        for veebileht in aeg_maha:
            domeen = veebileht[1]
            koik_lehed += [domeen]

            if veebileht[3] == 1 and not veebileht[5]:
                aeg = muuda_aega(domeen)
                if aeg <= 0:
                    threading.Thread(target=koosta_kysimus, args=(domeen,), daemon=True).start()
                muudetud_ajad.append(domeen)

        print(muudetud_ajad)
        puhas_url = urlparse(url[0])

        domeen = puhas_url.netloc.lstrip('www.')
        if (domeen in koik_lehed and aeg_maha[koik_lehed.index(domeen)][3] != 1 and not
        aeg_maha[koik_lehed.index(domeen)][5]):
            print(f'{domeen} hakkan aega maha võtma')
            aeg = muuda_aega(domeen)
            print(aeg)
            if aeg <= 0:
                muuda_staatust(domeen)
                threading.Thread(target=koosta_kysimus, args=(domeen,), daemon=True).start()


        elif domeen in koik_lehed:
            print(f'{domeen} on blokeeritud')
        else:
            print(f'{domeen} pole nimekirjas')


        return jsonify({"status": "success"})
    else:
        blokeeritud = []
        for i in aeg_maha:
            if i[3] == 1:
                blokeeritud += [i[1]]
        print(f'blokeeritud on {blokeeritud}')
        return jsonify({'blokeeritud': blokeeritud})

def run_flask():
    app.run(port=5000)

@app.route('/ping')
def ping():
    return "pong", 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)

