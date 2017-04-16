import os
import json

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

@app.route('/<path:dataset>', methods=['GET'])
def test(dataset):
    results = dw.query(dataset, 'SELECT * FROM Tables')
    response = make_response(json.dumps({'tables': [row['tableName'] for row in results.table]}, indent=4))
    response.headers['Content-Type'] = 'application/json'
    return response

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    app.run(debug=False, port=port, host='0.0.0.0')

