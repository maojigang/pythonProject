from flask import Flask, jsonify, request
import json
app = Flask(__name__)

@app.route('/hello', methods=['POST'])
def hello_world():
    res = request.data.decode('utf-8')
    requestJson = json.loads(res)
    print(f"requestJson= {requestJson}")
    data = {'code': 0, 'msg': 'success', 'data': 'hello world'}
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

