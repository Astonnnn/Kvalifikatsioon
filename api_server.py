from flask import Flask, request, jsonify
from flask_cors import CORS
import time
app = Flask(__name__)
CORS(app)


@app.route('/tabs',methods=['POST'])

def receive_tabs(): #see funktsioon saab chrome extensionilt andmeb lahtiolevate tabide kohta
    data = request.get_json()
    urls = data.get("urls", [])
    print(f'Avatud aknad:')
    for url in urls:
        print(url)
    return jsonify({'status': 'success','tabs_received': len(data)})




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
