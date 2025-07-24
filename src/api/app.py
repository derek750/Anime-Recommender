from flask import Blueprint, Flask
from flask_cors import CORS
from jikan_api import jikan_api
from dataset_api import dataset_api

app = Flask(__name__)
CORS(app)
app.register_blueprint(jikan_api)
app.register_blueprint(dataset_api)

# source venv/bin/activate
# cd src/api
# python3 app.py

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)