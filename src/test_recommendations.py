import requests
import json

# Base URL for the API
BASE_URL = "http://127.0.0.1:5000/api"

def test_recommendation_system():
    """Test the content-based recommendation system"""
    
    print("🚀 Testing Anime Recommendation System")
    print("=" * 50)
    
    # 1. Check status
    print("\n1. Checking recommender status...")
    response = requests.get(f"{BASE_URL}/recommendations/status")
    if response.status_code == 200:
        status = response.json()
        print(f"   Initialized: {status['initialized']}")
        print(f"   Total anime: {status['total_anime']}")
    else:
        print(f"   Error: {response.status_code}")
    
    # 2. Initialize the recommender
    print("\n2. Initializing recommender system...")
    response = requests.post(f"{BASE_URL}/recommendations/initialize")
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ {result['message']}")
        print(f"   Total anime loaded: {result['total_anime']}")
    else:
        print(f"   ❌ Error: {response.json()}")
        return
    
    # 3. Search for an anime
    print("\n3. Searching for 'Naruto'...")
    response = requests.get(f"{BASE_URL}/recommendations/search?q=Naruto&limit=5")
    if response.status_code == 200:
        results = response.json()
        print(f"   Found {results['total']} results:")
        for anime in results['results'][:3]:
            print(f"   - ID: {anime['anime_id']}, Title: {anime['title']}")
            print(f"     Score: {anime['score']}, Genres: {anime['genres']}")
    
    # 4. Get recommendations by anime ID (using first Naruto result)
    if response.status_code == 200 and results['results']:
        anime_id = results['results'][0]['anime_id']
        print(f"\n4. Getting recommendations for anime ID {anime_id}...")
        
        response = requests.get(f"{BASE_URL}/recommendations/by-id/{anime_id}?limit=5")
        if response.status_code == 200:
            recommendations = response.json()
            print(f"   Found {recommendations['total']} recommendations:")
            for i, anime in enumerate(recommendations['recommendations'][:3], 1):
                print(f"   {i}. {anime['title']}")
                print(f"      Score: {anime['score']}, Similarity: {anime['similarity_score']:.3f}")
                print(f"      Genres: {anime['genres']}")
    
    # 5. Get recommendations by title
    print("\n5. Getting recommendations by title 'Attack on Titan'...")
    response = requests.get(f"{BASE_URL}/recommendations/by-title?title=Attack on Titan&limit=3")
    if response.status_code == 200:
        recommendations = response.json()
        print(f"   Found {recommendations['total']} recommendations:")
        for i, anime in enumerate(recommendations['recommendations'], 1):
            print(f"   {i}. {anime['title']}")
            print(f"      Score: {anime['score']}, Similarity: {anime['similarity_score']:.3f}")
    elif response.status_code == 404:
        print("   No anime found with that title")
    
    # 6. Get recommendations by genres
    print("\n6. Getting recommendations for genres 'Action, Adventure'...")
    response = requests.get(f"{BASE_URL}/recommendations/by-genres?genres=Action,Adventure&limit=3")
    if response.status_code == 200:
        recommendations = response.json()
        print(f"   Found {recommendations['total']} recommendations:")
        for i, anime in enumerate(recommendations['recommendations'], 1):
            print(f"   {i}. {anime['title']}")
            print(f"      Score: {anime['score']}, Similarity: {anime['similarity_score']:.3f}")
            print(f"      Genres: {anime['genres']}")
    
    print("\n✅ Testing completed!")

if __name__ == "__main__":
    try:
        test_recommendation_system()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API server.")
        print("Make sure the Flask server is running on http://127.0.0.1:5000")
    except Exception as e:
        print(f"❌ Error: {e}")
