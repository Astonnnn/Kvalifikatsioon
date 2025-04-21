from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/tabs',methods=['POST'])

def receive_tabs():
    data = request.get_json()
    print(f'Avatud aknad:')
    for tab in data:
        print(f'{tab.get('url')}')
    return jsonify({'status': 'success','tabs_received': len(data)})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
