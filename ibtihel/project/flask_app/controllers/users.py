# Import necessary modules from Flask
from flask import render_template, request, redirect, session, flash, abort
from flask_app import app
# Import User and Product models
from flask_app.models.user import User
from flask_app.models.product import Product
# Import Bcrypt for password hashing
from flask_bcrypt import Bcrypt
# Import CSRF protection error handler
from flask_wtf.csrf import CSRFError

# Initialize Bcrypt
bcrypt = Bcrypt(app)

# Route for the home page
@app.route('/')
def index():
    # Get 4 top rated products
    top_rated_products = Product.get_top_rated(limit=4)
    # Render index template with top products
    return render_template('index.html', top_rated_products=top_rated_products)

# Route for user registration (handles both GET and POST)
@app.route('/register', methods=['GET', 'POST'])
def register():
    # If GET request, show registration form
    if request.method == 'GET':
        return render_template('register.html')
    
    try:
        # Validate registration form data
        if not User.validate_registration(request.form):
            return redirect('/register')
        
        # Hash the password
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        # Prepare user data for database
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': pw_hash,
            'address': request.form['address']
        }
        # Save user and get their ID
        user_id = User.save(data)
        # Store user ID in session
        session['user_id'] = user_id
        # Set session to be permanent (30 minutes)
        session.permanent = True  
        return redirect('/products')
    except Exception as e:
        # Handle registration errors
        flash("Une erreur s'est produite lors de l'inscription", "register")
        return redirect('/register')

# Route for user login (handles both GET and POST)
@app.route('/login', methods=['GET', 'POST'])
def login():
    # If GET request, show login form
    if request.method == 'GET':
        return render_template('login.html')
    
    try:
        # Validate login form data
        if not User.validate_login(request.form):
            return redirect('/login')
        
        # Check if user exists
        user = User.get_by_email({'email': request.form['email']})
        if not user:
            flash("Email/mot de passe invalide", "login")
            return redirect('/login')
        
        # Verify password
        if not bcrypt.check_password_hash(user.password, request.form['password']):
            flash("Email/mot de passe invalide", "login")
            return redirect('/login')
        
        # Store user ID in session
        session['user_id'] = user.id
        # Set session to be permanent (30 minutes)
        session.permanent = True
        return redirect('/products')
    except Exception as e:
        # Handle login errors
        flash("Une erreur s'est produite lors de la connexion", "login")
        return redirect('/login')

# Route for user logout
@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    return redirect('/login')

# CSRF error handler
@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    # Flash message for expired session
    flash("La session a expiré. Veuillez réessayer.", "error")
    # Redirect to previous page or home
    return redirect(request.referrer or '/')