from flask_app.config.mySQLConnection import connectToMySQL
from flask import flash

class Rating:
    db = "recommender_db"
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.product_id = data['product_id']
        self.rating = data['rating']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO ratings (user_id, product_id, rating) 
            VALUES (%(user_id)s, %(product_id)s, %(rating)s)
            ON DUPLICATE KEY UPDATE rating = %(rating)s;
        """
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_user_ratings(cls, user_id):
        query = "SELECT * FROM ratings WHERE user_id = %(user_id)s ORDER BY created_at DESC;"
        results = connectToMySQL(cls.db).query_db(query, {'user_id': user_id})
        ratings = []
        if results:
            for rating in results:
                ratings.append(cls(rating))
        return ratings

    @classmethod
    def get_product_ratings(cls, product_id):
        query = "SELECT * FROM ratings WHERE product_id = %(product_id)s;"
        results = connectToMySQL(cls.db).query_db(query, {'product_id': product_id})
        ratings = []
        if results:
            for rating in results:
                ratings.append(cls(rating))
        return ratings

    @classmethod
    def get_average_rating(cls, product_id):
        query = """
            SELECT AVG(rating) as avg_rating 
            FROM ratings 
            WHERE product_id = %(product_id)s;
        """
        result = connectToMySQL(cls.db).query_db(query, {'product_id': product_id})
        if result[0]['avg_rating']:
            return round(float(result[0]['avg_rating']), 1)
        return 0