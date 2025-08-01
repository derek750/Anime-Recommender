import requests
from flask import Blueprint, jsonify
import pandas as pd
import io

dataset_api = Blueprint('dataset_api', __name__, url_prefix='/api')

@dataset_api.route('/dataset', methods=['GET'])
def get_data():

    data_url = "https://api.github.com/repos/LeoRigasaki/Anime-dataset/contents/data/raw"  
    response = requests.get(data_url)
    files = response.json()

    for file in files:
        if file['name'].startswith("anime_seasonal") and file['name'].endswith(".csv"):
            csv_url = file['download_url']
            break

    response = requests.get(csv_url)

    if response.status_code == 200:
        df = pd.read_csv(io.StringIO(response.text))
        df = df.where(pd.notnull(df), None)
        return jsonify(df.to_dict(orient='records'))
    else:
        return jsonify({'error': 'CSV fetch failed'}), 500

