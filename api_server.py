from flask import Flask, request, jsonify
from flask_cors import CORS
from andmebaas import *
from urllib.parse import urlparse
import threading
from PyQt5.QtCore import QObject, pyqtSignal

app = Flask(__name__)
CORS(app)

#Read 13-23 teeb kindlaks, et eksisteerib PyQt rakendus, et kuvada küsimus (PyQt suudab hallata ühte peaakent korraga, niiet küsimus ja pearakendus ei saa olla erinevad rakenduse)

class DialogSignals(QObject):
    show_dialog = pyqtSignal(str)

signals = None

def set_main_window(window):
    global signals
    signals = DialogSignals(window)

def generate_question(veebileht):
    signals.show_dialog.emit(veebileht)


@app.route('/tabs', methods=['POST', 'GET'])


def saa_ning_saada_andmeid():
    andmebaasi_andmed = kuva_veebilehed()

    #võtab chrome extensionilt vastu json formaadis andmed, milles kirjas praegu aktiivne veebisait
    if request.method == 'POST':
        andmed = request.get_json()
        aktiivne_veebileht = andmed.get("urls", [])
        print(f'Avatud aken: {aktiivne_veebileht[0]}')
        andmebaasi_veebilehed = [] #Siia kõik andmebaasis olevate veebilehtede URLid

        for andmebaasi_rida in andmebaasi_andmed:
            veebileht = andmebaasi_rida[1]
            andmebaasi_veebilehed += [veebileht]

            #Võtame blokeeritud veebilehtedelt aega maha
            if andmebaasi_rida[3] == 1 and not andmebaasi_rida[5]:
                aeg = muuda_aeg(veebileht)
                if aeg <= 0:
                    threading.Thread(target=generate_question, args=(veebileht,), daemon=True).start()

        #Kasutab urllib.parse moodulit, et puhastada veebilehe url algsele kujule, nagu RegEx (https://www.youtube.com/abcdefghij -> youtube.com)
        puhas_url = urlparse(aktiivne_veebileht[0])
        veebileht = puhas_url.netloc.lstrip('www.')

        #kontrollib, kas aktiivne veebileht on andmebaasis, blokeerimata ning küsimus pole hetkel ees
        if (veebileht in andmebaasi_veebilehed and andmebaasi_andmed[andmebaasi_veebilehed.index(veebileht)][3] != 1 and not
        andmebaasi_andmed[andmebaasi_veebilehed.index(veebileht)][5]):
            print(f'{veebileht} hakkan aega maha võtma')
            aeg = muuda_aeg(veebileht)

            #Võtab aktiivselt lehelt aega maha
            if aeg <= 0:
                muuda_staatus(veebileht)
                threading.Thread(target=generate_question, args=(veebileht,), daemon=True).start()

        elif veebileht in andmebaasi_veebilehed:
            print(f'{veebileht} on blokeeritud')
        else:
            print(f'{veebileht} pole nimekirjas')


        return jsonify({"status": "success"})

    #Vastavalt chrome extensioni soovile saadab json formaadis andmed blokeeritud veebilehtede kohta
    else:
        blokeeritud = []
        for i in andmebaasi_andmed:
            if i[3] == 1:
                blokeeritud += [i[1]]
        print(f'Blokeeritud on {blokeeritud}')
        return jsonify({'Blokeeritud': blokeeritud})


def run_flask():
    app.run(port=5000)


#Saadab chrome extensionile teate, et server töötab
@app.route('/ping')
def ping():
    return "pong", 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)

