import requests
from flask import Blueprint, jsonify
import pandas as pd
import io

dataset_api = Blueprint('dataset_api', __name__, url_prefix='/api')

@dataset_api.route('/dataset')
def get_data():
    csv_url = "https://raw.githubusercontent.com/LeoRigasaki/Anime-dataset/main/data/raw/anime_seasonal_20250723.csv"    
    response = requests.get(csv_url)

    if response.status_code == 200:
        df = pd.read_csv(io.StringIO(response.text))
        return jsonify(df.head(10).to_dict(orient='records'))
    else:
        return jsonify({'error': 'CSV fetch failed'}), 500

