from flask import Flask, request, json, abort, send_from_directory
import os
from influxdb import InfluxDBClient
from flask_cors import CORS

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'centos_top')

api = Flask(__name__,static_folder='react_app/build')
CORS(api)

@api.route('/', defaults={'path': ''})
@api.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(api.static_folder + '/' + path):
        return send_from_directory(api.static_folder, path)
    else:
        return send_from_directory(api.static_folder, 'index.html')

@api.route('/data', methods=['GET'])
def get_data():
 
    ip = request.args.get('ip')
    result = client.query('SELECT * FROM centos_processes WHERE "ip"=\''+ip+'\' ORDER BY time DESC limit 10')
    test = list(result.get_points())
    if len(test) == 0:
        abort(404)
    else:
        x = {"data":test}

    return json.dumps(x)

if __name__ == '__main__':
     api.run(use_reloader=True, port=5000, threaded=True)
