from flask import Blueprint, jsonify, request
import requests

jikan_api = Blueprint('jikan_api', __name__, url_prefix='/api') 

@jikan_api.route('/jikan')
def search_anime():
    query = request.args.get('q')
    url = f"https://api.jikan.moe/v4/anime?q={query}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return jsonify(data)
    else:
        error = response.json()
        return jsonify({'error': error}), response.status_code

