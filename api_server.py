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

def generate_question(domain):
    signals.show_dialog.emit(domain)


@app.route('/tabs', methods=['POST', 'GET'])
def receive_tabs():
    website_list = show_websites()
    if request.method == 'POST':
        data = request.get_json()
        url = data.get("urls", [])
        print(f'Avatud aken: {url[0]}')
        all_websites = []
        changed_websites = []
        for website in website_list:
            domain = website[1]
            all_websites += [domain]

            if website[3] == 1 and not website[5]:
                time = change_time(domain)
                if time <= 0:
                    threading.Thread(target=generate_question, args=(domain,), daemon=True).start()
                changed_websites.append(domain)

        print(changed_websites)
        puhas_url = urlparse(url[0])

        domain = puhas_url.netloc.lstrip('www.')
        print(domain)
        if (domain in all_websites and website_list[all_websites.index(domain)][3] != 1 and not
        website_list[all_websites.index(domain)][5]):
            print(f'{domain} hakkan aega maha võtma')
            time = change_time(domain)
            print(time)
            if time <= 0:
                change_status(domain)
                threading.Thread(target=generate_question, args=(domain,), daemon=True).start()


        elif domain in all_websites:
            print(f'{domain} on blokeeritud')
        else:
            print(f'{domain} pole nimekirjas')


        return jsonify({"status": "success"})
    else:
        blocked = []
        for i in website_list:
            if i[3] == 1:
                blocked += [i[1]]
        print(f'Blokeeritud on {blocked}')
        print(type(blocked))
        return jsonify({'Blokeeritud': blocked})

def run_flask():
    app.run(port=5000)

@app.route('/ping')
def ping():
    return "pong", 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)

