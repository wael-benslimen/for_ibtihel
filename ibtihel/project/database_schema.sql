-- Create the database
CREATE DATABASE IF NOT EXISTS recommender_db;
USE recommender_db;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    address TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create products table
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    genre VARCHAR(100),
    features TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create ratings table
CREATE TABLE IF NOT EXISTS ratings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating >= 0 AND rating <= 5),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    UNIQUE KEY unique_rating (user_id, product_id)
);

-- Insert some sample products
INSERT INTO products (title, description, genre, features) VALUES
('Product 1', 'Description of product 1', 'Electronics', 'Feature1, Feature2, Feature3'),
('Product 2', 'Description of product 2', 'Books', 'Feature1, Feature4, Feature5'),
('Product 3', 'Description of product 3', 'Electronics', 'Feature2, Feature3, Feature6'),
('Product 4', 'Description of product 4', 'Clothing', 'Feature1, Feature7, Feature8'),
('Product 5', 'Description of product 5', 'Books', 'Feature4, Feature5, Feature9');
('Product 5', 'Description of product 5', 'Books', 'Feature4, Feature5, Feature9');
('Product 5', 'Description of product 5', 'Books', 'Feature4, Feature5, Feature9');
('Product 5', 'Description of product 5', 'Books', 'Feature4, Feature5, Feature9');
('Product 5', 'Description of product 5', 'Books', 'Feature4, Feature5, Feature9');