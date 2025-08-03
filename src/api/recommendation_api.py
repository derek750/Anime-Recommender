from flask import Blueprint, jsonify, request
from recommender import recommender

recommendation_api = Blueprint('recommendation_api', __name__, url_prefix='/api')