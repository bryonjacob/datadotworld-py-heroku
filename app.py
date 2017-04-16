import os
import json
import redis

from datadotworld.config import Config
from datadotworld.datadotworld import DataDotWorld

from flask import Flask
from flask import request
from flask import make_response

config = Config(config_file_path='./.dwconfig')
config.auth_token = os.environ['DATADOTWORLD_TOKEN']
config.save()
dw = DataDotWorld(config=config)
#print(dw.query('bryon/odin-2015-2016', 'SELECT * FROM Tables'))


app = Flask(__name__)

r = redis.from_url(os.environ.get("REDIS_URL"))

@app.route('/tables/<path:dataset>', methods=['GET'])
def test(dataset):
    results = dw.query(dataset, 'SELECT * FROM Tables')
    response = make_response(json.dumps({'tables': [row['tableName'] for row in results.table]}, indent=4))
    response.headers['Content-Type'] = 'application/json'
    return response

@app.route('/count', methods=['GET'])
def count():
    response = make_response(str(r.incr('counter', 1)))
    response.headers['Content-Type'] = 'text/plain'
    return response

@app.errorhandler(Exception)
def all_exception_handler(error):
    print(error)
    return error, 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    app.run(debug=False, port=port, host='0.0.0.0')

