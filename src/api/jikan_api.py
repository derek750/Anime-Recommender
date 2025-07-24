from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

@app.route('/jikan')

def search_anime():
    query = request.args.get('q')
    url = f"https://api.jikan.moe/v4/anime?q={query}"
    response = requests.get(url)
    if(response.status_code) == 200:
        data = response.json()
    else:
        error = response.json()
        print(error)
    
