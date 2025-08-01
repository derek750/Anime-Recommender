from flask import Blueprint, jsonify, request
from recommender import recommender

recommendation_api = Blueprint('recommendation_api', __name__, url_prefix='/api')

@recommendation_api.route('/recommendations/initialize', methods=['POST'])
def initialize_recommender():
    """Initialize the recommender system by loading and preprocessing data"""
    try:
        # Load data
        if not recommender.load_data():
            return jsonify({'error': 'Failed to load anime dataset'}), 500
        
        # Preprocess data
        if not recommender.preprocess_data():
            return jsonify({'error': 'Failed to preprocess data'}), 500
        
        return jsonify({
            'message': 'Recommender system initialized successfully',
            'total_anime': len(recommender.df)
        })
    
    except Exception as e:
        return jsonify({'error': f'Initialization failed: {str(e)}'}), 500

@recommendation_api.route('/recommendations/by-id/<int:anime_id>')
def get_recommendations_by_id(anime_id):
    """Get recommendations based on anime ID"""
    try:
        num_recommendations = request.args.get('limit', 10, type=int)
        
        if recommender.df is None:
            return jsonify({'error': 'Recommender not initialized. Call /initialize first'}), 400
        
        recommendations = recommender.get_recommendations(anime_id, num_recommendations)
        
        if not recommendations:
            return jsonify({'error': 'Anime not found or no recommendations available'}), 404
        
        return jsonify({
            'anime_id': anime_id,
            'recommendations': recommendations,
            'total': len(recommendations)
        })
    
    except Exception as e:
        return jsonify({'error': f'Failed to get recommendations: {str(e)}'}), 500

@recommendation_api.route('/recommendations/by-title')
def get_recommendations_by_title():
    """Get recommendations based on anime title"""
    try:
        title = request.args.get('title')
        num_recommendations = request.args.get('limit', 10, type=int)
        
        if not title:
            return jsonify({'error': 'Title parameter is required'}), 400
        
        if recommender.df is None:
            return jsonify({'error': 'Recommender not initialized. Call /initialize first'}), 400
        
        recommendations = recommender.get_recommendations_by_title(title, num_recommendations)
        
        if not recommendations:
            return jsonify({'error': 'Anime not found or no recommendations available'}), 404
        
        return jsonify({
            'search_title': title,
            'recommendations': recommendations,
            'total': len(recommendations)
        })
    
    except Exception as e:
        return jsonify({'error': f'Failed to get recommendations: {str(e)}'}), 500

@recommendation_api.route('/recommendations/by-genres')
def get_recommendations_by_genres():
    """Get recommendations based on preferred genres"""
    try:
        genres_param = request.args.get('genres')
        num_recommendations = request.args.get('limit', 10, type=int)
        
        if not genres_param:
            return jsonify({'error': 'Genres parameter is required'}), 400
        
        # Parse genres (comma-separated)
        genres = [genre.strip() for genre in genres_param.split(',')]
        
        if recommender.df is None:
            return jsonify({'error': 'Recommender not initialized. Call /initialize first'}), 400
        
        recommendations = recommender.get_recommendations_by_genres(genres, num_recommendations)
        
        if not recommendations:
            return jsonify({'error': 'No recommendations available for these genres'}), 404
        
        return jsonify({
            'genres': genres,
            'recommendations': recommendations,
            'total': len(recommendations)
        })
    
    except Exception as e:
        return jsonify({'error': f'Failed to get recommendations: {str(e)}'}), 500

@recommendation_api.route('/recommendations/search')
def search_anime():
    """Search for anime by title to get anime IDs"""
    try:
        query = request.args.get('q')
        limit = request.args.get('limit', 10, type=int)
        
        if not query:
            return jsonify({'error': 'Query parameter (q) is required'}), 400
        
        if recommender.df is None:
            return jsonify({'error': 'Recommender not initialized. Call /initialize first'}), 400
        
        # Search in titles
        matches = recommender.df[
            recommender.df['title'].str.contains(query, case=False, na=False) |
            recommender.df['english_title'].str.contains(query, case=False, na=False)
        ].head(limit)
        
        results = []
        for _, anime in matches.iterrows():
            results.append({
                'anime_id': anime['anime_id'],
                'title': anime['title'],
                'english_title': anime['english_title'],
                'type': anime['type'],
                'score': anime['score'],
                'genres': anime['genres']
            })
        
        return jsonify({
            'query': query,
            'results': results,
            'total': len(results)
        })
    
    except Exception as e:
        return jsonify({'error': f'Search failed: {str(e)}'}), 500

@recommendation_api.route('/recommendations/status')
def get_recommender_status():
    """Get the current status of the recommender system"""
    try:
        is_initialized = recommender.df is not None
        total_anime = len(recommender.df) if is_initialized else 0
        
        return jsonify({
            'initialized': is_initialized,
            'total_anime': total_anime,
            'available_endpoints': [
                '/api/recommendations/initialize (POST)',
                '/api/recommendations/by-id/<anime_id>',
                '/api/recommendations/by-title?title=<title>',
                '/api/recommendations/by-genres?genres=<genre1,genre2>',
                '/api/recommendations/search?q=<query>',
                '/api/recommendations/status'
            ]
        })
    
    except Exception as e:
        return jsonify({'error': f'Status check failed: {str(e)}'}), 500
