import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import requests
import io
import re

class ContentBasedRecommender:
    def __init__(self):
        self.df = None
        self.tfidf_matrix = None
        self.cosine_sim = None
        self.feature_matrix = None
        self.scaler = StandardScaler()
        self.anime_indices = None
        
    def load_data(self):

        response = requests.get("http://127.0.0.1:5000/api/dataset")
    
        if response.status_code == 200:
            data = response.json()
            self.df = pd.DataFrame(data)
            return True
        return False
    
    def preprocess_data(self):
        """Preprocess the data for content-based filtering"""
        if self.df is None:
            return False
            
        # Create a copy for processing
        df_processed = self.df.copy()
        
        # Fill missing values
        df_processed['genres'] = df_processed['genres'].fillna('')
        df_processed['studios'] = df_processed['studios'].fillna('')
        df_processed['source'] = df_processed['source'].fillna('')
        df_processed['type'] = df_processed['type'].fillna('')
        df_processed['rating'] = df_processed['rating'].fillna('')
        df_processed['status'] = df_processed['status'].fillna('')
        
        # Create combined text features for TF-IDF
        df_processed['combined_features'] = (
            df_processed['genres'].astype(str) + ' ' +
            df_processed['studios'].astype(str) + ' ' +
            df_processed['source'].astype(str) + ' ' +
            df_processed['type'].astype(str) + ' ' +
            df_processed['rating'].astype(str) + ' ' +
            df_processed['status'].astype(str)
        )
        
        # Clean the combined features
        df_processed['combined_features'] = df_processed['combined_features'].apply(
            lambda x: re.sub(r'[^\w\s]', ' ', x.lower())
        )
        
        # Create TF-IDF matrix
        tfidf = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        self.tfidf_matrix = tfidf.fit_transform(df_processed['combined_features'])
        
        # Create numerical features matrix
        numerical_features = []
        
        # Score (normalized)
        scores = df_processed['score'].fillna(df_processed['score'].mean())
        numerical_features.append(scores.values.reshape(-1, 1))
        
        # Episodes (normalized)
        episodes = df_processed['episodes'].fillna(df_processed['episodes'].median())
        numerical_features.append(episodes.values.reshape(-1, 1))
        
        # Popularity (inverse normalized - lower rank = higher popularity)
        popularity = df_processed['popularity'].fillna(df_processed['popularity'].max())
        popularity = 1 / (popularity + 1)  # Inverse for better similarity
        numerical_features.append(popularity.values.reshape(-1, 1))
        
        # Combine numerical features
        if numerical_features:
            numerical_matrix = np.hstack(numerical_features)
            numerical_matrix = self.scaler.fit_transform(numerical_matrix)
            
            # Combine TF-IDF and numerical features
            self.feature_matrix = np.hstack([
                self.tfidf_matrix.toarray(),
                numerical_matrix
            ])
        else:
            self.feature_matrix = self.tfidf_matrix.toarray()
        
        # Calculate cosine similarity
        self.cosine_sim = cosine_similarity(self.feature_matrix)
        
        # Create anime index mapping
        self.anime_indices = pd.Series(
            df_processed.index, 
            index=df_processed['anime_id']
        ).drop_duplicates()
        
        self.df = df_processed
        return True
    
    def get_recommendations(self, anime_id, num_recommendations=10):
        """Get recommendations for a given anime ID"""
        if self.cosine_sim is None or self.anime_indices is None:
            return []
        
        try:
            # Get the index of the anime
            idx = self.anime_indices[anime_id]
            
            # Get similarity scores for all anime
            sim_scores = list(enumerate(self.cosine_sim[idx]))
            
            # Sort by similarity score (descending)
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            
            # Get top N similar anime (excluding the input anime itself)
            sim_scores = sim_scores[1:num_recommendations + 1]
            
            # Get anime indices
            anime_indices = [i[0] for i in sim_scores]
            
            # Get recommendations with similarity scores
            recommendations = []
            for i, score in sim_scores:
                anime_data = self.df.iloc[i].to_dict()
                anime_data['similarity_score'] = score
                recommendations.append(anime_data)
            
            return recommendations
            
        except KeyError:
            return []
    
    def get_recommendations_by_title(self, title, num_recommendations=10):
        """Get recommendations by anime title"""
        if self.df is None:
            return []
        
        # Find anime by title (case insensitive partial match)
        matches = self.df[
            self.df['title'].str.contains(title, case=False, na=False) |
            self.df['english_title'].str.contains(title, case=False, na=False)
        ]
        
        if matches.empty:
            return []
        
        # Use the first match
        anime_id = matches.iloc[0]['anime_id']
        return self.get_recommendations(anime_id, num_recommendations)
    
    def get_recommendations_by_genres(self, genres, num_recommendations=10):
        """Get recommendations based on preferred genres"""
        if self.df is None:
            return []
        
        # Create a virtual anime with the specified genres
        virtual_features = ' '.join(genres).lower()
        
        # Transform using the same TF-IDF vectorizer
        tfidf = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        # Fit on existing data and transform the virtual anime
        all_features = list(self.df['combined_features']) + [virtual_features]
        tfidf_matrix_extended = tfidf.fit_transform(all_features)
        
        # Calculate similarity with the virtual anime (last row)
        virtual_sim = cosine_similarity(
            tfidf_matrix_extended[-1:], 
            tfidf_matrix_extended[:-1]
        ).flatten()
        
        # Get top recommendations
        sim_scores = list(enumerate(virtual_sim))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[:num_recommendations]
        
        recommendations = []
        for i, score in sim_scores:
            anime_data = self.df.iloc[i].to_dict()
            anime_data['similarity_score'] = score
            recommendations.append(anime_data)
        
        return recommendations

# Global recommender instance
recommender = ContentBasedRecommender()