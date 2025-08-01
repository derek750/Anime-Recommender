from flask import Flask
from flask_cors import CORS
from jikan_api import jikan_api
from dataset_api import dataset_api
from recommendation_api import recommendation_api

app = Flask(__name__)
CORS(app)
app.register_blueprint(jikan_api)
app.register_blueprint(dataset_api)
app.register_blueprint(recommendation_api)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
