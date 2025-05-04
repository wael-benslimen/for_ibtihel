from flask import Flask, render_template
import os
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = os.urandom(32)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)

# Security configurations
app.config['SESSION_COOKIE_SECURE'] = True  # Cookies only sent over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to session cookie
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes session timeout
app.config['WTF_CSRF_TIME_LIMIT'] = 3600  # CSRF token expires after 1 hour

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500