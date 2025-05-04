from flask_app.config.mySQLConnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = "recommender_db"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.address = data['address']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO users (first_name, last_name, email, password, address)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(address)s);
        """
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            return cls(result[0])
        return None

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            return cls(result[0])
        return None

    @staticmethod
    def validate_registration(user):
        is_valid = True
        # Validation du prénom
        if len(user['first_name']) < 2:
            flash("Le prénom doit faire au moins 2 caractères", "register")
            is_valid = False
        
        # Validation du nom
        if len(user['last_name']) < 2:
            flash("Le nom doit faire au moins 2 caractères", "register")
            is_valid = False
        
        # Validation de l'email
        if not EMAIL_REGEX.match(user['email']):
            flash("Email invalide", "register")
            is_valid = False
        else:
            # Vérifier si l'email existe déjà
            data = {
                "email": user['email']
            }
            potential_user = User.get_by_email(data)
            if potential_user:
                flash("Cet email est déjà utilisé", "register")
                is_valid = False
        
        # Validation du mot de passe
        if len(user['password']) < 8:
            flash("Le mot de passe doit faire au moins 8 caractères", "register")
            is_valid = False
        elif user['password'] != user['confirm_password']:
            flash("Les mots de passe ne correspondent pas", "register")
            is_valid = False
        
        return is_valid

    @staticmethod
    def validate_login(user):
        is_valid = True
        if not EMAIL_REGEX.match(user['email']):
            flash("Email/mot de passe invalide", "login")
            is_valid = False
        if len(user['password']) < 1:
            flash("Email/mot de passe invalide", "login")
            is_valid = False
        return is_valid