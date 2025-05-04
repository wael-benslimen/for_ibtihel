from flask_app import app
from flask_app.controllers import users, products
import os

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limite la taille des requêtes à 16MB
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # Session expire après 30 minutes

if __name__ == "__main__":
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)

