from flask import render_template, request, redirect, session, jsonify
from flask_app import app
from flask_app.models.product import Product
from flask_app.models.rating import Rating
from flask_app.models.recommender import Recommender
from flask_app.config.auth import login_required

# Show all products page
@app.route('/products')
@login_required  # Ensures user is logged in
def products():
    # Get list of all products
    products = Product.get_all()
    return render_template('products.html', products=products)

# Show single product details
@app.route('/product/<int:id>')
@login_required
def show_product(id):
    # Get product by its ID
    data = {'id': id}
    product = Product.get_by_id(data)
    if not product:
        return redirect('/products')
    # Get similar products recommendations
    recommender = Recommender()
    similar_products = recommender.content_based_recommendations(id)
    return render_template('show_product.html', product=product, similar_products=similar_products)

# Handle product rating submission
@app.route('/rate/product', methods=['POST'])
@login_required
def rate_product():
    # Save user's rating for a product
    data = {
        'user_id': session['user_id'],
        'product_id': request.json['product_id'],
        'rating': request.json['rating']
    }
    Rating.save(data)
    return jsonify({'message': 'Rating saved successfully'}), 200

# Show personalized recommendations
@app.route('/recommendations')
@login_required
def get_recommendations():
    recommender = Recommender()
    # Get user's previous ratings
    user_ratings = Rating.get_user_ratings(session['user_id'])
    
    if user_ratings:
        # Use last rated product for recommendations
        last_rated_product = user_ratings[-1].product_id
        recommendations = recommender.hybrid_recommendations(
            session['user_id'], 
            last_rated_product
        )
    else:
        # If no ratings, show top-rated products
        recommendations = Product.get_top_rated(limit=4)
    
    return render_template('recommendations.html', recommendations=recommendations)