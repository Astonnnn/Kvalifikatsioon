from flask import Flask, request, jsonify
from flask_cors import CORS
from database import *
import time
app = Flask(__name__)
CORS(app)
import threading
mainwindow_ref = None


def set_main_window_reference(window):
    global mainwindow_ref
    mainwindow_ref = window
    return mainwindow_ref


a = 1 #Paneb käima recieve tabs koodi
print(a)

@app.route('/tabs',methods=['POST'])

def receive_tabs():#see funktsioon saab chrome extensionilt andmeb lahtiolevate tabide kohta
    global a #muutes seda ui.py saab panna selle kui pausile küsimuse ajaks
    if a == 1:
        data = request.get_json()
        print(data)
        urls = data.get("urls", [])
        print(f'Avatud aknad: {urls}')
        aeg_maha = kuva_veebilehed()
        koik_lehed = []
        print(aeg_maha)
        for veebileht in aeg_maha:
            koik_lehed += [veebileht[1]]
        for url in urls:
            i = url.find('://')
            url = url[i+3:] #Võtab kõik pärast //:
            i = url.find('/')
            url = url[:i] #Võtab kõik enne
            url = url.strip('www.')
            url = url.strip()
            if url in koik_lehed:
                for veeb in aeg_maha: #muudab staatuse tagasi üheks kui juba ei ole
                    if veeb[1] == url:
                        stat = veeb[3]
                        if stat == 1:
                            muuda_staatust(url)
                            break
                print(f'{url} hakkan aega maha võtma')
                aeg = muuda_aega(url)
                print(aeg)
                if aeg <= 0:
                    muuda_staatust(url)
                    mainwindow_ref.trigger_signal.emit() #Teatab mainwindow klassile, et genereeriks kysimuse
                    a = 0
                    print(url)
                    taasta_aeg(url)
                    return jsonify({"status": "Triggered"}), 200,
            else:
                print(f'{url} ei hakka maha võtma')

        return jsonify({'status': 'success','tabs_received': len(data)})
    else:
        data = request.get_json()
        print(f'{a} e a väärtus ei ole muutunud')
        return jsonify({'status': 'success', 'tabs_received': len(data)})
def run_flask():
    app.run(port=5000)

@app.route('/ping')
def ping():
    return "pong", 200


if __name__ == '__main__':
    app.run( port=5000, debug=True)


