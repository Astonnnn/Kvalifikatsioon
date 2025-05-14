from flask import Flask, request, jsonify
from flask_cors import CORS
from database import *
import time
app = Flask(__name__)
CORS(app)

@app.route('/tabs',methods=['POST'])

def receive_tabs(): #see funktsioon saab chrome extensionilt andmeb lahtiolevate tabide kohta
    data = request.get_json()
    print(data)
    urls = data.get("urls", [])
    print(f'Avatud aknad: {urls}')
    aeg_maha = kuva_veebilehed()
    koik_lehed = []
    for veebileht in aeg_maha:
        koik_lehed += [veebileht[1]]
    for url in urls:
        i = url.find('://')
        url = url[i+3:] #Võtab kõik pärast //:
        i = url.find('/')
        url = url[:i] #Võtab kõik enne /
        url = url.strip('www.')
        url = url.strip()
        if url in koik_lehed:
            print(f'{url} hakkan aega maha võtma')
        else:
            print(f'{url} ei hakka maha võtma')
    return jsonify({'status': 'success','tabs_received': len(data)})

@app.route('/ping')
def ping():
    return "pong", 200


if __name__ == '__main__':
    app.run( port=5000, debug=True)


