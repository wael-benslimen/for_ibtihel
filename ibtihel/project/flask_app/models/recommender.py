from flask_app.config.mySQLConnection import connectToMySQL
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import nltk
import re

# Download required NLTK data for text processing
nltk.download('punkt')

class Recommender:
    def __init__(self):
        # Initialize text vectorizer to convert text to numbers
        self.tfidf = TfidfVectorizer(stop_words='english')
        # Initialize word stemmer to reduce words to their root form
        self.ps = PorterStemmer()
        # Database name constant
        self.db = "recommender_db"

    def preprocess_text(self, text):
        # Handle empty or missing text
        if pd.isna(text) or not text:
            return ""
        
        # Convert text to lowercase for consistency
        text = str(text).lower()
        
        # Remove special characters, keep only letters and spaces
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        try:
            # Split text into individual words
            tokens = word_tokenize(text)
        except LookupError:
            # Fallback to simple splitting if NLTK fails
            tokens = text.split()
        
        # Convert words to their root form (e.g., 'running' -> 'run')
        stemmed_tokens = [self.ps.stem(token) for token in tokens]
        
        # Combine processed words back into text
        return ' '.join(stemmed_tokens)

    def content_based_recommendations(self, product_id, n_recommendations=4):
        # Get all products from database
        query = "SELECT * FROM products;"
        products = connectToMySQL(self.db).query_db(query)
        
        if not products:
            return []

        # Convert products to pandas DataFrame for easier processing
        df = pd.DataFrame(products)
        # Process product features for comparison
        df['processed_features'] = df['features'].apply(self.preprocess_text)
        
        # Convert text features to number vectors
        tfidf_matrix = self.tfidf.fit_transform(df['processed_features'])
        
        # Calculate similarity between products
        cosine_sim = cosine_similarity(tfidf_matrix)
        euclidean_sim = 1 / (1 + euclidean_distances(tfidf_matrix))
        
        # Combine different similarity measures
        combined_sim = (cosine_sim + euclidean_sim) / 2
        
        # Find target product's position
        product_idx = df[df['id'] == product_id].index[0]
        
        # Get similarity scores for all products
        sim_scores = list(enumerate(combined_sim[product_idx]))
        # Sort by similarity
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get top N most similar products (excluding the product itself)
        sim_scores = sim_scores[1:n_recommendations+1]
        product_indices = [i[0] for i in sim_scores]
        
        # Return similar products' details
        return df.iloc[product_indices][['id', 'title', 'description', 'genre']].to_dict('records')

    def collaborative_filtering_recommendations(self, user_id, n_recommendations=4):
        # Retrieve all user ratings from the database
        query = """
            SELECT user_id, product_id, rating 
            FROM ratings;
        """
        ratings = connectToMySQL(self.db).query_db(query)
        
        if not ratings:
            return []

        # Create a user-product rating matrix
        df_ratings = pd.DataFrame(ratings)
        ratings_matrix = df_ratings.pivot(
            index='user_id', 
            columns='product_id', 
            values='rating'
        ).fillna(0)

        # Calculate similarity between users
        user_similarity = cosine_similarity(ratings_matrix)
        
        # Find the index of the target user
        user_idx = ratings_matrix.index.get_loc(user_id)
        
        # Get the most similar users
        similar_users = list(enumerate(user_similarity[user_idx]))
        similar_users = sorted(similar_users, key=lambda x: x[1], reverse=True)
        similar_users = similar_users[1:5]  # Top 4 similar users
        
        # Retrieve recommended products
        recommendations = []
        user_rated_products = set(df_ratings[df_ratings['user_id'] == user_id]['product_id'])
        
        for sim_user_idx, _ in similar_users:
            sim_user_id = ratings_matrix.index[sim_user_idx]
            sim_user_ratings = df_ratings[df_ratings['user_id'] == sim_user_id]
            
            # Filter products the user hasn't rated yet
            new_products = sim_user_ratings[
                ~sim_user_ratings['product_id'].isin(user_rated_products)
            ]
            
            recommendations.extend(new_products[new_products['rating'] >= 4]['product_id'])
        
        # Retrieve details of recommended products
        if recommendations:
            query = """
                SELECT id, title, description, genre 
                FROM products 
                WHERE id IN %(product_ids)s 
                LIMIT %(limit)s;
            """
            recommendations = list(set(recommendations))[:n_recommendations]
            data = {
                'product_ids': recommendations,
                'limit': n_recommendations
            }
            return connectToMySQL(self.db).query_db(query, data)
        
        return []

    def hybrid_recommendations(self, user_id, product_id, n_recommendations=4):
        # Get recommendations from both approaches
        content_based = self.content_based_recommendations(product_id, n_recommendations)
        collaborative = self.collaborative_filtering_recommendations(user_id, n_recommendations)
        
        # Combine recommendations
        all_recommendations = content_based + collaborative
        
        # Remove duplicates while maintaining priority order
        seen = set()
        unique_recommendations = []
        for rec in all_recommendations:
            if rec['id'] not in seen:
                seen.add(rec['id'])
                unique_recommendations.append(rec)
        
        return unique_recommendations[:n_recommendations]