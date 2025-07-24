import requests
from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

app.route('/dataset')

def get_data():
    csv_url = "https://github.com/LeoRigasaki/Anime-dataset/blob/main/data/raw/anime_seasonal_20250723.csv"
    response = requests.get(csv_url)

    if response.status_code == 200:
        df = pd.read_csv(pd.compat.StringIO(response.text))
        return jsonify(df.head(10).to_dict(orient='records'))
    else:
        return jsonify({'error': 'CSV fetch failed'}), 500

