import requests
from flask import Blueprint, jsonify
import pandas as pd
import io
from animetype import Anime
from typing import List, cast

dataset_api = Blueprint('dataset_api', __name__, url_prefix='/api')

def convert_pd_anime(df: pd.DataFrame) -> List[Anime]:
    records = df.where(pd.notnull(df), None).to_dict(orient='records')
    anime_list = []
    
    for record in records:
        anime_item = cast(Anime, record)
        anime_list.append(anime_item)
    
    return anime_list

@dataset_api.route('/dataset', methods=['GET'])
def get_data():

    data_url = "https://api.github.com/repos/LeoRigasaki/Anime-dataset/contents/data/raw"  
    response = requests.get(data_url)
    files = response.json()

    for file in files:
        if file['name'].startswith("anime_seasonal") and file['name'].endswith(".csv"):
            csv_url = file['download_url']
            break

    response : pd.DataFrame = requests.get(csv_url)

    if response.status_code == 200:
        df = pd.read_csv(io.StringIO(response.text))
        data = convert_pd_anime(df)
        return jsonify(data)
    else:
        return jsonify({'error': 'CSV fetch failed'}), 500

