from flask_app.config.mySQLConnection import connectToMySQL
from flask_app.models.rating import Rating
from flask import flash

class Product:
    db = "recommender_db"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.genre = data['genre']
        self.features = data['features']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.average_rating = 0

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM products;"
        results = connectToMySQL(cls.db).query_db(query)
        products = []
        if results:
            for product in results:
                p = cls(product)
                p.average_rating = Rating.get_average_rating(p.id)
                products.append(p)
        return products

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM products WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            product = cls(result[0])
            product.average_rating = Rating.get_average_rating(product.id)
            return product
        return None

    @classmethod
    def get_top_rated(cls, limit=4):
        query = """
            SELECT p.*, AVG(r.rating) as avg_rating 
            FROM products p 
            LEFT JOIN ratings r ON p.id = r.product_id 
            GROUP BY p.id 
            ORDER BY avg_rating DESC 
            LIMIT %(limit)s;
        """
        results = connectToMySQL(cls.db).query_db(query, {'limit': limit})
        products = []
        if results:
            for product in results:
                p = cls(product)
                p.average_rating = float(product['avg_rating']) if product['avg_rating'] else 0
                products.append(p)
        return products