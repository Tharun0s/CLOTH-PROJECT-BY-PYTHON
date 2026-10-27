
from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from pathlib import Path

app = Flask(__name__)
app.secret_key = "threadly_secret_key_123"

# MySQL database configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123456789",
    "database": "threadly_store"
}

ADMIN_PASSWORD = "123456789"


# Connect to MySQL
def get_db():
    return mysql.connector.connect(**DB_CONFIG)


# Create tables and sample products
def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(150) NOT NULL,
            category VARCHAR(80) NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            image_url TEXT NOT NULL,
            description TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            customer_name VARCHAR(150) NOT NULL,
            phone VARCHAR(30) NOT NULL,
            address TEXT NOT NULL,
            product_name VARCHAR(150) NOT NULL,
            quantity INT NOT NULL,
            total DECIMAL(10,2) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]

    if count == 0:
        products = [
            ("Classic T-Shirt", "Men", 499,
             "https://placehold.co/400x500?text=T-Shirt",
             "Comfortable cotton T-shirt"),

            ("Casual Shirt", "Men", 799,
             "https://placehold.co/400x500?text=Shirt",
             "Stylish casual shirt"),

            ("Summer Dress", "Women", 999,
             "https://placehold.co/400x500?text=Dress",
             "Beautiful summer dress"),

            ("Denim Jeans", "Men", 1199,
             "https://placehold.co/400x500?text=Jeans",
             "Everyday denim jeans"),

            ("Kurti", "Women", 699,
             "https://placehold.co/400x500?text=Kurti",
             "Traditional casual kurti"),

            ("Hoodie", "Unisex", 899,
             "https://placehold.co/400x500?text=Hoodie",
             "Soft everyday hoodie")
        ]

        cursor.executemany("""
            INSERT INTO products
            (name, category, price, image_url, description)
            VALUES (%s, %s, %s, %s, %s)
        """, products)

    conn.commit()
    cursor.close()
    conn.close()


@app.route("/")
def home():
    category = request.args.get("category", "All")

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT DISTINCT category FROM products")
    categories = [row["category"] for row in cursor.fetchall()]

    if category == "All":
        cursor.execute("SELECT * FROM products ORDER BY id DESC")
    else:
        cursor.execute(
            "SELECT * FROM products WHERE category = %s ORDER BY id DESC",
            (category,)
        )

    products = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "index.html",
        products=products,
        categories=categories,
        selected_category=category
    )


@app.route("/checkout", methods=["POST"])
def checkout():
    customer_name = request.form.get("customer_name", "").strip()
    phone = request.form.get("phone", "").strip()
    address = request.form.get("address", "").strip()
    product_name = request.form.get("product_name", "").strip()

    try:
        quantity = int(request.form.get("quantity", "1"))
        price = float(request.form.get("price", "0"))

        if quantity < 1 or price < 0:
            raise ValueError
    except (ValueError, TypeError):
        flash("Invalid quantity or price.")
        return redirect(url_for("home"))

    if not all([customer_name, phone, address, product_name]):
        flash("Please fill in all required fields.")
        return redirect(url_for("home"))

    # Get the actual product price from the database
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT price FROM products WHERE name = %s",
        (product_name,)
    )
    product = cursor.fetchone()

    if product is None:
        cursor.close()
        conn.close()
        flash("Product not found.")
        return redirect(url_for("home"))

    # Calculate total using database price, not the submitted price
    total = float(product["price"]) * quantity

    cursor.execute("""
        INSERT INTO orders
        (customer_name, phone, address, product_name, quantity, total)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        customer_name,
        phone,
        address,
        product_name,
        quantity,
        total
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return render_template(
        "success.html",
        customer_name=customer_name,
        product_name=product_name,
        quantity=quantity,
        total=total
    )


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        password = request.form.get("password", "")

        if password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("admin"))

        flash("Incorrect admin password.")

    if not session.get("admin_logged_in"):
        return render_template("admin_login.html")

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM orders ORDER BY id DESC")
    orders = cursor.fetchall()

    cursor.execute("SELECT * FROM products ORDER BY id DESC")
    products = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "admin.html",
        orders=orders,
        products=products
    )


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin"))


if __name__ == "__main__":
    try:
        init_db()
        print("MySQL connected successfully!")
        print("Threadly running at http://127.0.0.1:5000")
        app.run(debug=True)
    except mysql.connector.Error as error:
        print("MySQL Database Error:", error)
        print("Check MySQL is running, database name, username and password.")
