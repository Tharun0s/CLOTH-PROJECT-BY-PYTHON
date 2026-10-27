-- Optional MySQL starter schema (the app itself uses SQLite by default).
-- Demo admin password requested: 123456789 (used by Flask demo login, not a MySQL account).
CREATE DATABASE IF NOT EXISTS threadly_store;
USE threadly_store;

CREATE TABLE IF NOT EXISTS products (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150) NOT NULL,
  category VARCHAR(80) NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  image_url TEXT NOT NULL,
  description TEXT
);

CREATE TABLE IF NOT EXISTS orders (
  id INT AUTO_INCREMENT PRIMARY KEY,
  customer_name VARCHAR(150) NOT NULL,
  phone VARCHAR(30) NOT NULL,
  address TEXT NOT NULL,
  product_name VARCHAR(150) NOT NULL,
  quantity INT NOT NULL,
  total DECIMAL(10,2) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
