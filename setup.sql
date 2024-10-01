-- Create the database
CREATE DATABASE IF NOT EXISTS product_database;

-- Use the newly created database
USE product_database;

-- Create a products table
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,   -- Unique identifier for each product
    name VARCHAR(255) NOT NULL,          -- Name of the product
    price DECIMAL(10, 2) NOT NULL,       -- Price of the product
    stock ENUM('In Stock', 'Out of Stock') NOT NULL,  -- Stock status
    category VARCHAR(100),                -- Category of the product
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,   -- Timestamp when the product was added
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  -- Timestamp when the product was updated
);

-- Optional: Create a table for product categories if you want to manage categories separately
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,    -- Unique identifier for each category
    name VARCHAR(100) NOT NULL UNIQUE,    -- Name of the category
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Timestamp when the category was added
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  -- Timestamp when the category was updated
);

-- Optional: Create a foreign key relation between products and categories
ALTER TABLE products
ADD CONSTRAINT fk_category
FOREIGN KEY (category) REFERENCES categories(name);
